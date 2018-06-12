# Coding:uft-8
import re
import math
import time
import requests
import threading

class MyThread(threading.Thread):

    pageRange = range(1,1)

    url = "http://www.xxx.xxx/movie/list_23_%s.html"

    prefix = "http://www.xxx.xxx%s"

    def __init__(self,argument):

        threading.Thread.__init__(self)
        
        self.name = argument[0]

        self.pageRange = argument[1]

    def run(self):

        print ("%s：任务开始"%self.name)
        
        try:

            for page in self.pageRange:

                print("%s：正在爬取第%s页\n"%(self.name,page))

                url = self.url

                self.MainSpider(url%(page))

                print("%s：爬取第%s页完成\n"%(self.name,page))

            print ("%s：任务完成"%self.name)

        except Exception as err:

            with open ("ErrorLog.txt","a",encoding='utf-8') as f:

                f.write("%s：%s：%s\n"%(self.localTime(),self.name,str(err)))

            print ("%s：异常结束"%self.name)

    def MainSpider(self,url):

        try:
            
            response = requests.get(url)

            response.encoding = "gb2312"

            ruler = '<a href="(.*?)" class="ulink">(.*?)</a>'

            movieList = re.findall(ruler,response.text)

            for movie in movieList:

                self.MovieSpider(movie)

        except requests.exceptions.ConnectionError as err:

            with open ("FailLog.txt","a",encoding='utf-8') as f:

                f.write("%s：%s：%s：%s\n"%(self.localTime(),self.name,str(err),url))


    def MovieSpider(self,movie):

        try:

            print("%s：发现电影《%s》\n"%(self.name,movie[1]))

            movieURL = self.prefix%movie[0]

            response = requests.get(movieURL)

            response.encoding = "gbk"

            ruler = r'<td style="WORD-WRAP: break-word" bgcolor="#fdfddf">.*?<a href="(.*?)">.*?</a>'

            LinkList = re.findall(ruler,response.text)

            with open ("MovieSpider/%s.txt"%(self.name),"a",encoding='utf-8') as f:

                f.write("片名：%s\n"%movie[1])

                f.write("地址：%s\n"%movieURL)

                if len(LinkList)>0:

                    for Link in LinkList:

                        f.write("下载：%s\n"%(Link))
                else:

                    f.write("下载：抱歉，没有获取到\n")

                f.write("\n--------------------------------------------------\n")
                
        except requests.exceptions.ConnectionError as err:

            with open ("FailLog.txt","a",encoding='utf-8') as f:

                f.write("%s：%s：%s：%s\n"%(self.localTime(),self.name,str(err),movieURL))

    def localTime(self):

        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


def GetPageCount():

    try:
        
        url = 'http://www.xxx.xxx/movie/index.html'

        response = requests.get(url)

        response.encoding = "gb2312"

        ruler = '<td height="25" align="center".*?共([0-9]*?)页'

        PageCount = re.findall(ruler,response.text)

        if len(PageCount)>0:

            return PageCount[0]

    except:

        return 0

def RunTask(PageCount):
    
    maxPage = PageCount

    maxThread = 10

    threadPage = math.ceil(maxPage / maxThread)

    instance = math.ceil(maxPage / threadPage)

    Threads = []

    ThreadID = 0

    starttime = time.time()

    for Thread in range(0,instance):

        startPage = 1 + threadPage * (ThreadID)

        endedPage = threadPage * (ThreadID + 1)

        if endedPage > maxPage : endedPage = maxPage

        ThreadName = "Thread_%s"%(str(ThreadID).zfill(len(str(maxThread))))

        Thread = MyThread((ThreadName,range(startPage,endedPage + 1)))

        Threads.append(Thread)

        Thread.start()

        if endedPage > maxPage : break

        ThreadID += 1

    for Thread in Threads:

        while not isinstance(Thread, MyThread):

            time.sleep(1)

            pass

        Thread.join()

    endtime = time.time()

    print ("\n--任务结束--\n")
    print ("最大线程数：%s\n"%maxThread)
    print ("任务总数量：%s\n"%maxPage)
    print ("线程处理量：%s\n"%threadPage)
    print ("启动线程数：%s\n"%instance)
    print ("运行总耗时：%s\n"%str(endtime - starttime))

if __name__ == "__main__":

    PageCount = GetPageCount()

    #PageCount = 175
    
    if PageCount == 0:
        print("获取页码失败")
    else:
        RunTask(int(PageCount))



    




