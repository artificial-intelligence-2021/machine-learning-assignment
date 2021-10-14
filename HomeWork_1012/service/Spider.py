import requests
from bs4 import BeautifulSoup
import shutil
import os

class SpiderService(object):
    def set_url(self,url):
        self.__url__ = url
        self.__status__ = self.__check_url__(url)
        
    def __check_url__(self,url):
        if "https://mil.news.sina.com.cn/" not in url:
            print("您输入的网页可能不是新浪军事频道哦")
            return False
        elif "57918" not in url[-5:]:
            print("输入的地址不是中国军情频道地址,请检查")
    def get_pages(self,pages_cnt = 25):
        if self.__status__:
            print("输入的页面地址不正确,无法获取内容")
        else:
            res_home = requests.get(self.__url__)
            if res_home.status_code == 200:
                self.__process_text__ = ""
                self.__process_text__ = "开始获取新闻页面,请稍后..."    
#                 清空目录
                shutil.rmtree('news_file', ignore_errors=True)
                os.mkdir('news_file')
                print(self.__process_text__)
                self.__start__(pages_cnt)
                print("="*50)
                print(f"完成页面内容下载,详细内容请查看同目录下说明文件")
                self.__write_log__()
            else:        
                print("无法找到页面")            
            pass
    def __start__(self,pages_cnt):
        for page_num in range(1,pages_cnt + 1):
            res_page = requests.get(f'{self.__url__}&page={page_num}')
            if res_page.status_code == 200:
                res_page.encoding = res_page.apparent_encoding # 设置编码格式                
                self.__process_text__ += f"\n\n开始获取第{page_num}页新闻内容\n"
                self.__process_text__ += "\n---\n"
                print(f"开始获取第{page_num}页新闻内容")
                print("="*50)
#                 建立页面文件夹
                self.__current_folder__ = f'news_file/page_{str(page_num).zfill(2)}'
                os.makedirs(self.__current_folder__)                
                self.__capture_link__(res_page)
            else:        
                print("无法找到页面") 
    def __capture_link__(self, res_page):
        soup = BeautifulSoup(res_page.text, "html.parser")
        self.__article_nums__ = 0
#       抓取新闻区域
        news_ul = soup.find_all(name = "ul", attrs = {"class":"linkNews"})
        for news_li in news_ul:
#           获取每一个超级链接标签
            news = news_li.find_all(name="a")          
            for new in news:
                self.__article_nums__ += 1
                self.__capture_page_content__(new.get("href"),new.text)      

    def __capture_page_content__(self,page_url,title):
        res_page = requests.get(page_url)
        if res_page.status_code == 200:
                res_page.encoding = res_page.apparent_encoding # 设置编码格式       
                print(f"正在抓取新闻: {title}")
                self.__capture_content__(res_page,title)
        else:        
            print(f"无法找到 {title} 新闻页面,请检查地址: {page_url}") 
        pass
    def __capture_content__(self,res_page,title_txt):
        soup = BeautifulSoup(res_page.text, "html.parser")
#       抓取新闻标题
        title = soup.find(name = "h1", attrs = {"class":"main-title"})
        div_body = soup.find_all(name = "div",attrs = {"class":"article"})
        body_text = ""
        for body in div_body:
            contents = body.find_all(name="p")
            for content in contents:
                body_text += content.text + "\n\n"
        file_path = f"{self.__current_folder__}/article_{str(self.__article_nums__).zfill(2)}.md"
        try:
            with open(file = file_path, mode = "w", encoding = "utf-8") as f:            
                f.write(f"## {title.text}\n")
                f.write(f"{body_text}")
            self.__process_text__ += f"\n- 已完成新闻: [{title.text}]({file_path}) 内容的抓取"
        except Exception as ex: # 异常处理
            print(f"新闻: {title_txt}下载失败,发生异常:{ex}")
            self.__process_text__ += f"\n- 未完成新闻: {title_txt} 内容的抓取,出现异常:{ex}"
    def __write_log__(self):
        with open(file = "新浪新闻.md", mode = "w", encoding = "utf-8") as f:
            f.write(self.__process_text__)