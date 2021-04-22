from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from datetime import datetime, timedelta, timezone, date
import datetime
import time
import pyperclip
import re


# 할 일
# 1. 서로이웃 꽉 찼을 때 인식 고치기

"""

12시가 되면 5000명의 카테고리에서 균등하게 총 100명을 삭제한다.
삭제는 활동이 가장 적은 사람으로 선택한다.

# 서로이웃 신청이 들어온 목록을 확인한다.
# 이 중 신청 양식에 맞춰 보내준 사람을 오래된 순으로 수락하고, 양식에 맞추지 않게 보낸 사람은 거절한다.

만약 서로이웃 신청이 없으면,
서로이웃 카테고리들을 확인한다.
한 카테고리 당 500에서 카테고리의 사람 수를 빼고, 그만큼 추가한다.
한 카테고리 당 최대 인원 수에서 10명 씩 삭제.(총 100명)
"""

id = 'more_neighbors'
ps = 'Sje7314123@'
search = "코딩"
want_categorys = ["IT"]


def txt_count():  # 오늘 날짜를 읽어, count함수를 받아온다.
    global count
    global today
    today = date.today()
    print(str(today))
    try:
        f = open(
            "C:/project/more_neighbors/naver_blog/blog.txt", 'x')
        print(" [더많은 서로이웃] 베타적 생성 성공")
        count = 0
        f.write(str(today) + "\n")
        f.write(str(count))
        f.close()
        print(" [더많은 서로이웃] 더많은 서로이웃 처음 시작")
        print(" [더많은 서로이웃] "+str(today)+"일 더많은 서로이웃 시작.")
        print(" [더많은 서로이웃] count = 0, 카운트 변수를 새로 지정함")
        print("")
    except:
        f = open(
            "C:/project/more_neighbors/naver_blog/blog.txt", 'r')
        before_txt_date = f.readline()
        print(" [더많은 서로이웃] 날짜는 : "+before_txt_date)
        if before_txt_date == str(today) + '\n':
            count = f.readline(2)
            f.close()
            if count != "":
                print(" [더많은 서로이웃] 오늘의 기록이 있습니다.\n카운트를 " +
                      str(count)+"부터 이어서 시작합니다!")
            elif count == "":
                count = 0
                print(" [오류 발생] 카운트를 0으로 설정합니다")
            print("")
        else:
            f.close()
            f = open(
                "C:/project/more_neighbors/naver_blog/blog.txt", 'w')
            f.write(str(today) + "\n")
            count = 0
            f.write(str(count))
            f.close()
            print(" [더많은 서로이웃] 새로운 날짜입니다.\n카운트를 0으로 지정합니다!")
            print("")


def blogToMblog():  # 지금 있는 블로그 형태의 사이트 주소 -> 모바일 블로그로 변환후 돌려줌.
    blogURL = (driver.current_url)  # 블로그의 주소를 blogURL 변수에 저장
    blogeridPrint = re.compile("com/(\w+)")  # 아이디 부분을 출력하는 정규식
    BPbloger = blogeridPrint.search(str(blogURL))  # 정규식을 사용하여 저장
    blogerid = BPbloger.group(1)  # 정규식을 사용하여 저장

    i = open(
        "C:/project/more_neighbors/naver_blog/BANNED_ID_LIST.txt", 'r')
    read = i.read()  # 메모장 읽어오기
    No_ADD_IDS = read.split("\n")  # 아이디들을 리스트에 저장
    i.close()  # 메모장 닫기
    mblog = False  # 블로그 주소 변수 저장, False면 스킵, 아니면 블로그 주소 접속
    loop_in = True  # 루프에 들어가 있으면 True 아니면 루프를 바로 나감
    for No_ADD_ID in No_ADD_IDS:
        if loop_in != True:
            continue
        if str(blogerid) == str(No_ADD_ID):
            print(" [더많은 서로이웃] 차단 아이디 발견!")
            print(" [더많은 서로이웃] 해당 아이디를 차단함")
            print("")
            loop_in = False
        else:
            mblog = ('https://m.blog.naver.com/' +
                     str(blogerid))  # 블로그 주소를 모바일 형태로 변환
    return mblog


def back(forplay):
    while 0 != forplay:
        time.sleep(0.5)
        driver.back()
        forplay -= 1
    return


def bloger_ban():  # 지금 있는 블로그 형태의 사이트를 차단 목록에 추가함.
    blogURL = (driver.current_url)  # 블로그의 주소를 blogURL 변수에 저장
    blogeridPrint = re.compile("com/(\w+)")  # 아이디 부분을 출력하는 정규식
    BPbloger = blogeridPrint.search(str(blogURL))  # 정규식을 사용하여 저장
    blogerid = BPbloger.group(1)  # 정규식을 사용하여 저장

    i = open(
        "C:/project/more_neighbors/naver_blog/BANNED_ID_LIST.txt", 'a')
    i.write(blogerid+'\n')
    i.close()


def neighbors_del():  # 모든 카테고리의 이웃을 삭제함
    global category_num1
    global category_num2
    global category_num3
    global category_num4
    global category_num5
    global category_num6
    global category_num7
    global category_num8
    global category_num9
    global category_num10
    driver.get('https://admin.blog.naver.com/'+str(id))
    driver.implicitly_wait(1)

    driver.find_element_by_id("buddylist_config_anchor").click()
    time.sleep(1)
    driver.switch_to.frame(driver.find_element_by_id('papermain'))
    loop_play1 = True
    neighbor_category_num = 2
    while loop_play1 == True:
        driver.find_element_by_xpath(
            '/html/body/div[1]/form/table/thead/tr/th[2]/div/div[1]/span').click()

        time.sleep(1)
        try:
            driver.find_element_by_xpath(
                '/html/body/div[1]/form/table/thead/tr/th[2]/div/div[2]/ul/li['+str(neighbor_category_num)+']').click()
            if neighbor_category_num == 2:
                category_num1 = 500 - int(category_mans)
                print(" [더많은 서로이웃] 1번 카테고리는 " +
                      str(category_num1)+"명을 더 추가할 수 있습니다.")
            if neighbor_category_num == 3:
                category_num2 = 500 - int(category_mans)
                print(" [더많은 서로이웃] 2번 카테고리는 " +
                      str(category_num2)+"명을 더 추가할 수 있습니다.")
            if neighbor_category_num == 4:
                category_num3 = 500 - int(category_mans)
                print(" [더많은 서로이웃] 3번 카테고리는 " +
                      str(category_num3)+"명을 더 추가할 수 있습니다.")
            if neighbor_category_num == 5:
                category_num4 = 500 - int(category_mans)
                print(" [더많은 서로이웃] 4번 카테고리는 " +
                      str(category_num4)+"명을 더 추가할 수 있습니다.")
            if neighbor_category_num == 6:
                category_num5 = 500 - int(category_mans)
                print(" [더많은 서로이웃] 5번 카테고리는 " +
                      str(category_num5)+"명을 더 추가할 수 있습니다.")
            if neighbor_category_num == 7:
                category_num6 = 500 - int(category_mans)
                print(" [더많은 서로이웃] 6번 카테고리는 " +
                      str(category_num6)+"명을 더 추가할 수 있습니다.")
            if neighbor_category_num == 8:
                category_num7 = 500 - int(category_mans)
                print(" [더많은 서로이웃] 7번 카테고리는 " +
                      str(category_num7)+"명을 더 추가할 수 있습니다.")
            if neighbor_category_num == 9:
                category_num8 = 500 - int(category_mans)
                print(" [더많은 서로이웃] 8번 카테고리는 " +
                      str(category_num8)+"명을 더 추가할 수 있습니다.")
            if neighbor_category_num == 10:
                category_num9 = 500 - int(category_mans)
                print(" [더많은 서로이웃] 9번 카테고리는 " +
                      str(category_num9)+"명을 더 추가할 수 있습니다.")
            if neighbor_category_num == 11:
                category_num10 = 500 - int(category_mans)
                print(" [더많은 서로이웃] 10번 카테고리는 " +
                      str(category_num10)+"명을 더 추가할 수 있습니다.")

        except:
            print(" [더많은 서로이웃] "+str(neighbor_category_num - 1) +
                  "번째 카테고리에서 오류가 발생했습니다.")
            loop_play1 = False
            continue
        time.sleep(1)
        neighbor_category_num += 1
        driver.find_element_by_xpath(
            '/html/body/div[1]/form/table/thead/tr/th[3]/div/div[1]/span').click()
        driver.find_element_by_xpath(
            '/html/body/div[1]/form/table/thead/tr/th[3]/div/div[2]/ul/li[2]').click()

        loop_play2 = True
        x = 1
        while loop_play2 == True:
            try:
                elem = driver.find_element_by_xpath(
                    '//*[@id="buddyListManageForm"]/table/tbody/tr['+str(x) + ']/td[4]/div/a')
                x += 1
                elem = elem.get_attribute("href")
                blogeridPrint = re.compile("com/(\w+)")  # 아이디 부분을 출력하는 정규식
                BPbloger = blogeridPrint.search(str(elem))  # 정규식을 사용하여 저장
                blogerid = BPbloger.group(1)  # 정규식을 사용하여 저장
                print(" [더많은 서로이웃] "+blogerid+"의 이웃을 삭제함")

                i = open("C:/stockauto/selenium/BANNED_ID_LIST.txt", 'a')
                i.write(blogerid+'\n')
                i.close()
            except:
                loop_play2 = False

        driver.find_element_by_xpath(
            '//*[@id="buddyListManageForm"]/table/thead/tr/th[1]/input').click()  # 체크박스 클릭
        try:
            driver.find_element_by_xpath(
                '//*[@id="buddyListManageForm"]/div[1]/div[1]/span[3]/button').click()  # 삭제버튼 클릭
            driver.find_element_by_xpath(
                '//*[@id="tpl_layer_del"]/div/div/fieldset/div/input').click()
            print(" [더많은 서로이웃] "+str(x)+"명 삭제됨")
        except:
            pass
        driver.find_element_by_xpath(
            '/html/body/div[1]/form/table/thead/tr/th[3]/div/div[1]/span').click()  # 이웃란 클릭
        driver.find_element_by_xpath(
            '/html/body/div[1]/form/table/thead/tr/th[3]/div/div[2]/ul/li[1]').click()  # 모든 이웃 보기
        category_mans = driver.find_element_by_xpath(
            '/html/body/div[1]/form/div[1]/div[2]/span/strong').text  # 이웃 수 다운로드


def date_neighbor_del():
    driver.get('https://admin.blog.naver.com/'+str(id))
    driver.implicitly_wait(1)
    NowDate = datetime.datetime.now()
    times = []
    mday = 0
    for p in range(3):
        SubtractTime = NowDate - timedelta(days=mday)
        FormatDate0 = datetime.datetime.strftime(SubtractTime, '%y.%m.%d.')
        times.append(FormatDate0)
        mday += 1
    # print(times)
    driver.find_element_by_id("buddyinvite_config_anchor").click()
    time.sleep(2)
    driver.switch_to.frame(driver.find_element_by_id('papermain'))

    driver.find_element_by_xpath(
        '//*[@id="inviteMe"]/ul/li[2]').click()  # 서로이웃 신청 리스트 열기
    time.sleep(2)
    invite_page = 1
    btn_num = 1
    loop = True
    Find = True
    Find_Find = True
    while loop == True:
        try:
            Find = False
            # print(times)
            topdate = driver.find_element_by_xpath(
                '//*[@id="invite"]/table/tbody/tr['+str(btn_num)+']/td[4]').text
            # print("이 블로거의 날짜는 "+str(topdate))
            dayCheck = False
            for timeplay in times:
                # print(timeplay)
                if dayCheck == True:
                    print("[Skip]")
                    continue
                if timeplay == str(topdate):
                    # print("이 블로거는 3일이 지나지 않음")
                    dayCheck = True
                    Find = True
                    continue
                elif timeplay != str(topdate):
                    # print("이 블로거는 3일이 지남")
                    pass

                else:
                    print("오류")
            if dayCheck == False:
                driver.find_element_by_xpath(
                    '//*[@id="invite"]/table/tbody/tr['+str(btn_num)+']/td[1]/input').click()
                # print(" [!!!!]클릭!")
            btn_num += 1
        except:
            btn_num = 1
            driver.find_element_by_xpath(
                '//*[@id="invite"]/div[3]/div/span[2]/button').click()  # 서로이웃 신청 취소
            time.sleep(1)
            try:
                Find = True
                result = driver.switch_to_alert()
                # print(result.text)
                result.accept()
                time.sleep(1)
                result = driver.switch_to_alert()
                result.accept()
                time.sleep(1)
                if Find_Find == False:
                    Find = False
                Find_Find = False

            except:
                Find = False
                print("alert를 찾지 못함")

            if Find == False:
                try:
                    driver.find_element_by_xpath(
                        '/html/body/div/form[2]/div[4]/a['+str(invite_page)+']')
                    if page == 2:
                        if page == True:
                            page = False
                        elif page == False:
                            page += 1
                        # 다음 페이지로 이동
                    invite_page += 1
                except:
                    print("이 카테고리는 마무리됨")
                    loop = False
                    continue


def add_neighbors():  # 서로이웃을 검색어를 이용하여 서로이웃을 추가함z
    page = 1
    neighbors_add = 0  # 서로이웃 추가 반복 횟수 변수
    global search
    global today
    global count
    global category_num1
    global category_num2
    global category_num3
    global category_num4
    global category_num5
    global category_num6
    global category_num7
    global category_num8
    global category_num9
    global category_num10
    global cate_FULL1
    global cate_FULL2
    global cate_FULL3
    global cate_FULL4
    global cate_FULL5
    global cate_FULL6
    global cate_FULL7
    global cate_FULL8
    global cate_FULL9
    global cate_FULL10
    global search_var

    cate_FULL1 = False
    cate_FULL2 = False
    cate_FULL3 = False
    cate_FULL4 = False
    cate_FULL5 = False
    cate_FULL6 = False
    cate_FULL7 = False
    cate_FULL8 = False
    cate_FULL9 = False
    cate_FULL10 = False
    while int(count) < 100:  # 메인 루프, 기본 카테고리 넘버, 검색어 설정
        if cate_FULL1 == False:
            if category_num1 > 0:  # 프로그래밍
                search_var = 1
                if page > 50:
                    add_neighbors2()
                    continue
                elif page <= 0:
                    search = "코딩"
        if cate_FULL2 == False:
            if category_num1 > 0:  # 사업
                search_var = 2
                if page > 50:
                    add_neighbors2()
                    continue
                elif page <= 0:
                    search = "창업"
        # elif cate_FULL3 == False:
        #     if category_num3 > 0:
        #         search = "검색어를 입력해주세요"
        #         search_var = 3
        # elif cate_FULL4 == False:
        #     if category_num4 > 0:
        #         search = "검색어를 입력해주세요"
        #         search_var = 4
        # elif cate_FULL5 == False:
        #     if category_num5 > 0:
        #         search = "검색어를 입력해주세요"
        #         search_var = 5
        # elif cate_FULL6 == False:
        #     if category_num6 > 0:
        #         search = "검색어를 입력해주세요"
        #         search_var = 6
        # elif cate_FULL7 == False:
        #     if category_num7 > 0:
        #         search = "검색어를 입력해주세요"
        #         search_var = 7
        # elif cate_FULL8 == False:
        #     if category_num8 > 0:
        #         search = "검색어를 입력해주세요"
        #         search_var = 8
        # elif cate_FULL9 == False:
        #     if category_num9 > 0:
        #         search = "검색어를 입력해주세요"
        #         search_var = 9
        # elif cate_FULL10 == False:
        #     if category_num10 > 0:
        #         search = "검색어를 입력해주세요"
        #         search_var = 10
        else:
            break
            print("카테고리가 모두 가득 차있음.")
        if search == False:
            continue
        print("최초 검색")
        # 검색어, 최신순으로 검색
        while int(count) < 100:  # 메인 루프2, 페이지 변경, 블로거 불러오기
            print("최초 검색2")
            if eval('cate_FULL'+str(search_var)) == True:
                print(str(search_var)+"번째 카테고리가 가득 참.")
                break
            if page > 50:
                break
            driver.get(
                'http://section.blog.naver.com/Search/Post.nhn?pageNo=' + str(page) + '&rangeType=ALL&orderBy=recentdate&keyword=' + str(search))  # 페이지 이동
            driver.implicitly_wait(5)  # 5초 암묵적 대기
            print(" [더많은 서로이웃] 검색어 이동 완료")

            blogers = driver.find_elements_by_class_name(
                "author")  # 검색으로 나온 이웃들 프로필 위치를 bloger 변수로 저장
            driver.implicitly_wait(5)

            for bloger in blogers:
                neighbors_add += 1
                bloger.click()  # 전부 클릭

                time.sleep(0.5)  # 클릭 후 0.5초 씩 대기
            print(" [더많은 서로이웃] 블로거  출력 끝")

            while neighbors_add > 0:  # 한 페이지에 7명, 전부 다운로드
                if eval('cate_FULL'+str(search_var)) == True:
                    break
                print(" [더많은 서로이웃] "+str(neighbors_add) + "번째 블로거를 염")
                driver.switch_to.window(
                    driver.window_handles[-1])  # 반복 횟수의 페이지를 염
                neighbors_add -= 1  # 그 페이지 x번째 탭

                URL = blogToMblog()
                if str(URL) == 'https://m.blog.naver.com/Search':
                    print(" 알 수 없는 오류가 발생했습니다. 프로그램에 조정값을 적용합니다.")
                    break
                elif URL != False:
                    driver.get(URL)  # 네이버 로그인 창으로 이동
                    print(" [더많은 서로이웃] "+str(URL) + "(아이디) 이동 완료")
                    time.sleep(1)

                driver.implicitly_wait(3)  # 3초 암묵적 대기

                try:
                    category = driver.find_element_by_xpath(
                        '/html/body/ui-view/bg-nsc/div[7]/div[1]/div[1]/div[2]/span[2]/div/span[1]').text
                except:
                    print(" [더많은 서로이웃] 카테고리 없음 창을 닫음")
                    driver.close()
                    continue
                print("카테고리 = " + str(category))
                try:
                    for want_category in want_categorys:  # 카테고리와 맞을 경우, 서로이웃을 신청
                        if eval('cate_FULL'+str(search_var)) == True:
                            break
                        if want_category in category:
                            print(" [더많은 서로이웃] "+str(category)+"카테고리 포함됨")
                            driver.find_element_by_xpath(
                                "/html/body/ui-view/bg-nsc/div[7]/div[1]/div[2]/div/div[1]/a").click()  # 서로이웃 신청 버튼 클릭
                            time.sleep(1)

                            try:
                                # 이미 서로이웃 진행 중일 때 닫음
                                if driver.find_element_by_id("_confirmLayerOk"):
                                    driver.close()
                                    continue
                            except:
                                print("서로이웃 신청 중이 아님")

                            print("서로이웃 시작")

                            try:
                                # 서로이웃이 열려있다면
                                if driver.find_element_by_id('bothBuddyRadio').is_enabled():
                                    driver.find_element_by_id(
                                        'bothBuddyRadio').click()  # 서로이웃 누르기
                                    time.sleep(0.5)

                                    # 카테고리 선택
                                    if search_var == 1:
                                        driver.find_element_by_xpath(
                                            '//*[@id="buddyGroupSelect"]/option[1]').click()  # 몇번째 카테고리 선택
                                        category_num1 -= 1
                                    elif search_var == 2:
                                        driver.find_element_by_xpath(
                                            '//*[@id="buddyGroupSelect"]/option[2]').click()  # 몇번째 카테고리 선택
                                        category_num2 -= 1
                                    elif search_var == 3:
                                        driver.find_element_by_xpath(
                                            '//*[@id="buddyGroupSelect"]/option[3]').click()  # 몇번째 카테고리 선택
                                        category_num3 -= 1
                                    elif search_var == 4:
                                        driver.find_element_by_xpath(
                                            '//*[@id="buddyGroupSelect"]/option[4]').click()  # 몇번째 카테고리 선택
                                        category_num4 -= 1
                                    elif search_var == 5:
                                        driver.find_element_by_xpath(
                                            '//*[@id="buddyGroupSelect"]/option[5]').click()  # 몇번째 카테고리 선택
                                        category_num5 -= 1
                                    elif search_var == 6:
                                        driver.find_element_by_xpath(
                                            '//*[@id="buddyGroupSelect"]/option[6]').click()  # 몇번째 카테고리 선택
                                        category_num6 -= 1
                                    elif search_var == 7:
                                        driver.find_element_by_xpath(
                                            '//*[@id="buddyGroupSelect"]/option[7]').click()  # 몇번째 카테고리 선택
                                        category_num7 -= 1
                                    elif search_var == 8:
                                        driver.find_element_by_xpath(
                                            '//*[@id="buddyGroupSelect"]/option[8]').click()  # 몇번째 카테고리 선택
                                        category_num8 -= 1
                                    elif search_var == 9:
                                        driver.find_element_by_xpath(
                                            '//*[@id="buddyGroupSelect"]/option[9]').click()  # 몇번째 카테고리 선택
                                        category_num9 -= 1
                                    elif search_var == 10:
                                        driver.find_element_by_xpath(
                                            '//*[@id="buddyGroupSelect"]/option[10]').click()  # 몇번째 카테고리 선택
                                        category_num10 -= 1

                                    else:
                                        print("카테고리가 모두 가득 차있음.")
                                        continue

                                    time.sleep(0.5)
                                    # 멘트 적기
                                    bloger_name = driver.find_element_by_class_name(
                                        "name").text  # 상대 닉네임 bloger_name에 저장
                                    elem = driver.find_element_by_xpath(
                                        '//*[@id="buddyAddForm"]/fieldset/div/div[2]/div[3]/div/textarea')
                                    elem.clear()  # 멘트 창 초기화
                                    # 서로이웃 메세지 설정
                                    elem.send_keys(
                                        "안녕하세요. " + str(bloger_name) + "!\n서로 이웃 신청해봅니다.")
                                    driver.find_element_by_class_name(
                                        "btn_ok").click()  # 보내기 버튼 누르기
                                    time.sleep(0.5)
                                    print("서로이웃 보낸 후 닫음")

                                    time.sleep(2)
                                    try:
                                        print("서로이웃 초과 확인")
                                        full_cate = driver.find_element_by_xpath(
                                            '//*[@id="_alertLayerClose"]')
                                        print("이 카테고리의 인원수가 가득참")
                                        if full_cate == True:
                                            driver.close()
                                            if cate_FULL1 == False:
                                                cate_FULL1 = True
                                            elif cate_FULL2 == False:
                                                cate_FULL2 = True
                                            elif cate_FULL3 == False:
                                                cate_FULL3 = True
                                            elif cate_FULL4 == False:
                                                cate_FULL4 = True
                                            elif cate_FULL5 == False:
                                                cate_FULL5 = True
                                            elif cate_FULL6 == False:
                                                cate_FULL6 = True
                                            elif cate_FULL7 == False:
                                                cate_FULL7 = True
                                            elif cate_FULL8 == False:
                                                cate_FULL8 = True
                                            elif cate_FULL9 == False:
                                                cate_FULL9 = True
                                            elif cate_FULL10 == False:
                                                cate_FULL10 = True
                                            count -= 1
                                            break
                                    except:
                                        print("초과 아님")
                                    count = int(count) + 1
                                    print("오늘 하루, "+str(count) + "명 추가됨")
                                    driver.close()  # 탭 닫음
                                    print("(블로거) "+str(bloger_name) +
                                          " 에게 서로이웃을 신청함")
                                    time.sleep(0.5)
                                    today2 = date.today()
                                    if today != today2:
                                        print(
                                            "서로이웃 추가 중, 날짜의 변경이 인식되었습니다.\n카운트를 초기화합니다.")
                                        count = 1
                                        f = open(
                                            "C:/project/more_neighbors/naver_blog/blog.txt", 'w')
                                        today = date.today()
                                        f.write(str(today) + "\n")
                                        f.write(str(count))
                                        f.close()
                                    else:
                                        f = open(
                                            "C:/project/more_neighbors/naver_blog/blog.txt", 'w')
                                        f.write(str(today) + "\n")
                                        f.write(str(count))
                                        f.close()
                                    continue

                                else:
                                    print("서로이웃을 받지 않음")
                                    driver.close()  # 탭 닫음
                                    continue

                                if driver.find_element_by_id('r2'):
                                    pass
                                elif driver.find_element_by_id('r1'):
                                    driver.close()  # 탭 닫음
                                    continue
                                else:
                                    print("서로 이웃을 거절 한 이웃임")
                                    bloger_ban()
                                    driver.find_element_by_id(
                                        'r2').click()  # 서로이웃 삭제 누르기
                                    driver.find_element_by_class_name(
                                        "btn_ok").click()  # 보내기 버튼 누르기
                                    driver.close()  # 탭 닫음
                                    continue
                            except:
                                pass
                        else:
                            print(str(category)+"카테고리임, " +
                                  str(want_category)+"가 아님")
                            continue
                    print("카운트 : " + str(count))
                    driver.close()  # 탭 닫음
                    pass
                except:
                    pass
            page += 1  # 페이지 수
            time.sleep(1)
            driver.switch_to.window(
                driver.window_handles[0])  # 검색할 수 있는 페이지로 이동
            time.sleep(1)
            print("이 카테고리 인원 수 : "+str(eval('category_num'+str(search_var))))
            if eval('category_num'+str(search_var)) == 0:
                continue
        if eval('category_num'+str(search_var)) == 0:
            continue
        search = False

    print("서로이웃 추가를 종료")

    if neighbors_add != 0:
        try:
            for q in range(neighbors_add):
                driver.switch_to.window(driver.window_handles[-1])
                driver.close()
        except:
            pass
    driver.switch_to.window(driver.window_handles[-1])


def add_neighbors2():
    driver.get('https://admin.blog.naver.com/'+str(id))  # 블로그 정보란 이동
    driver.implicitly_wait(1)

    driver.find_element_by_id("buddylist_config_anchor").click()  # 서로이웃 정보란 이동
    time.sleep(1)
    driver.switch_to.frame(driver.find_element_by_id('papermain'))  # 프레임 변경

    driver.find_element_by_xpath(
        '/html/body/div[1]/form/table/thead/tr/th[2]/div/div[1]/span').click()     # 서로이웃 카테고리 선택창 염
    search_vars = search_var + 1
    driver.find_element_by_xpath(
        '/html/body/div[1]/form/table/thead/tr/th[2]/div/div[2]/ul/li['+str(search_vars)+']').click()  # 서로이웃 카테고리 1번 선택
    search_vars = search_var - 1
    print(" [더 많은 서로이웃] 서로이웃 카테고리 변경 완료!")
    page = 1
    get_page = True
    page_2 = True
    while get_page == True:
        if eval('cate_FULL'+str(search_var)) == True:
            break
        neighbors_add = 1  # 팝업 창 갯수 세기
        loop_play = True  # 서로이웃 열기 반복문의 반복 여부를 참으로 변경
        while loop_play == True:  # 서로이웃을 전부 열때까지 반복
            try:
                driver.find_element_by_xpath(
                    '//*[@id="buddyListManageForm"]/table/tbody/tr[' + str(neighbors_add) + ']/td[4]/div/a').click()  # neighbors_add번째 서로이웃 클릭
                neighbors_add += 1  # neighbors_add를 더함

            except:  # 서로이웃을 전부 열면 루프 정지
                print("끝")
                loop_play = False
        neighbors_add -= 1  # 창 값 조정
        print(str(neighbors_add)+"명의 서로이웃을 열었습니다.")  # x 값 프린트

        time.sleep(2)
        while neighbors_add > 0:
            if eval('cate_FULL'+str(search_var)) == True:
                break
            driver.switch_to.window(driver.window_handles[-1])  # 반복 횟수의 페이지를 염
            neighbors_add -= 1  # 그 페이지 x번째 탭

            URL = blogToMblog()
            if URL != False:
                driver.get(URL)  # 네이버 로그인 창으로 이동
                time.sleep(1)

            driver.find_element_by_xpath(
                '//*[@id="rego_cover"]/div[1]/div[2]/div/div[3]/a[2]').click()
            neis_nei_index = 1
            argoorism_count = 0
            argorism = True
            while argorism == True:

                if eval('cate_FULL'+str(search_var)) == True:
                    print("블로그 카테고리가 꽉 차있음, "+str(search_var)+"번째 카테고리\n")
                    break
                if argoorism_count >= 6:
                    argorism = False
                    print("알고리즘 초과, 다음 블로거를 염")
                    continue

                try:
                    adbtn = driver.find_element_by_xpath(
                        "/html/body/ui-view/bg-nsc/div[5]/div/div/div[2]/div/div[4]/a[1]")
                    if adbtn == True:
                        argoorism_count = 0
                        back(1)
                except:
                    pass

                try:
                    driver.find_element_by_xpath(
                        '//*[@id="ct"]/div[1]/div/ul/buddy['+str(neis_nei_index)+']/li/div/div[1]/a').click()
                except:
                    print("서로이웃을 찾지 못함")
                    argorism = False
                    continue
                neis_nei_index += 1

                URL = blogToMblog()
                if URL == False:
                    argoorism_count += 1
                    print("argoorism_count : "+str(argoorism_count)+"..")
                elif URL != False:
                    driver.get(URL)  # 네이버 로그인 창으로 이동
                    time.sleep(1)
                    try:
                        adbtn = driver.find_element_by_xpath(
                            "/html/body/ui-view/bg-nsc/div[5]/div/div/div[2]/div/div[4]/a[1]")
                        if adbtn:
                            back(1)
                    except:
                        pass

                    try:
                        category = driver.find_element_by_xpath(
                            '/html/body/ui-view/bg-nsc/div[7]/div[1]/div[1]/div[2]/span[2]/div/span[1]').text
                        if category:
                            print("카테고리 있음")
                    except:
                        print("카테고리 없음")
                        back(1)
                    print("카테고리 = " + str(category))
                    print("원하는 카테고리 = " + str(want_categorys)+"\n")
                    try:
                        for want_category in want_categorys:
                            if want_category in category:
                                print("카테고리 포함됨")
                                argoorism_count = 0
                                print(
                                    " [더 많은 서로이웃] 원하는 카테고리의 블로거를 찾아 알고리즘 넘버가 초기화되었습니다.")
                                driver.find_element_by_xpath(
                                    "/html/body/ui-view/bg-nsc/div[7]/div[1]/div[2]/div/div[1]/a").click()  # 서로이웃 신청 버튼 클릭
                                time.sleep(2)

                                print("시작")
                                try:
                                    if driver.find_element_by_xpath('//*[@id="_confirmLayerOk"]'):  # 이미 서로이웃 신청 중일 때\
                                        print("서로이웃 신청중임")
                                        # print("서로이웃 신청 중임")
                                        driver.find_element_by_xpath(
                                            '//*[@id="_confirmLayercancel"]').click()
                                        # time.sleep(1)
                                        back(1)
                                        continue
                                except:
                                    print("서로이웃 신청 중이 아님")

                                print("서로이웃 시작")

                                try:
                                    # 서로이웃이 열려있다면
                                    if driver.find_element_by_id('bothBuddyRadio').is_enabled():
                                        driver.find_element_by_id(
                                            'bothBuddyRadio').click()  # 서로이웃 누르기
                                        time.sleep(0.5)
                                        driver.find_element_by_xpath(
                                            '//*[@id="buddyGroupSelect"]/option[1]').click()  # 몇번째 카테고리 선택

                                        time.sleep(0.5)
                                        elem = driver.find_element_by_xpath(
                                            '//*[@id="buddyAddForm"]/fieldset/div/div[2]/div[3]/div/textarea')  # 서로이웃 멘트 창을 elme 변수로 저장
                                        bloger_name = driver.find_element_by_class_name(
                                            "name").text  # 상대 닉네임 bloger_name에 저장
                                        elem.clear()  # 멘트 창 초기화
                                        # 서로이웃 메세지 설정
                                        elem.send_keys(
                                            "안녕하세요. " + str(bloger_name) + "!\n서로 이웃 신청해봅니다.")
                                        time.sleep(0.5)
                                        driver.find_element_by_class_name(
                                            "btn_ok").click()  # 보내기 버튼 누르기
                                        time.sleep(0.5)
                                        try:
                                            print("서로이웃 초과 확인")
                                            full_cate = driver.find_element_by_xpath(
                                                '//*[@id="_alertLayerClose"]')
                                            print("이 카테고리의 인원수가 가득참")
                                            if full_cate == True:
                                                driver.close()
                                                if cate_FULL1 == False:
                                                    cate_FULL1 = True
                                                elif cate_FULL2 == False:
                                                    cate_FULL2 = True
                                                elif cate_FULL3 == False:
                                                    cate_FULL3 = True
                                                elif cate_FULL4 == False:
                                                    cate_FULL4 = True
                                                elif cate_FULL5 == False:
                                                    cate_FULL5 = True
                                                elif cate_FULL6 == False:
                                                    cate_FULL6 = True
                                                elif cate_FULL7 == False:
                                                    cate_FULL7 = True
                                                elif cate_FULL8 == False:
                                                    cate_FULL8 = True
                                                elif cate_FULL9 == False:
                                                    cate_FULL9 = True
                                                elif cate_FULL10 == False:
                                                    cate_FULL10 = True
                                                count -= 1
                                                break
                                        except:
                                            print("초과 아님")

                                        count = int(count) + \
                                            1  # 서로이웃 보낸 수 +1
                                        today2 = date.today()
                                        if today != today2:
                                            print(
                                                "서로이웃 추가 중, 날짜의 변경이 인식되었습니다.\n카운트를 초기화합니다.")
                                            count = 1
                                            f = open(
                                                "C:/project/more_neighbors/naver_blog/blog.txt", 'w')
                                            today = date.today()
                                            f.write(str(today) + "\n")
                                            f.write(str(count))
                                            f.close()
                                        else:
                                            f = open(
                                                "C:/project/more_neighbors/naver_blog/blog.txt", 'w')
                                            f.write(str(today) + "\n")
                                            f.write(str(count))
                                            f.close()

                                        back(2)
                                        continue
                                    else:
                                        print("서로이웃을 받지 않음")
                                        back(2)
                                        continue

                                    if driver.find_element_by_id('r2'):
                                        pass
                                    elif driver.find_element_by_id('r1'):
                                        back(2)  # 탭 닫음
                                        continue
                                    else:
                                        print("서로 이웃을 거절 한 이웃임")
                                        bloger_ban()
                                        driver.find_element_by_id(
                                            'r2').click()  # 서로이웃 삭제 누르기
                                        driver.find_element_by_class_name(
                                            "btn_ok").click()  # 보내기 버튼 누르기
                                        back(2)  # 탭 닫음
                                        continue
                                except:
                                    pass
                            else:
                                print(str(category)+"카테고리임, " +
                                      str(want_category)+"가 아님")
                                argoorism_count += 1
                                print("argoorism_count : " +
                                      str(argoorism_count)+"..")
                                back(1)
                                continue
                        print("카운트 : " + str(count))
                    except:
                        pass
                print("창 닫음")
            driver.close()

        try:
            driver.find_element_by_xpath(
                '/html/body/div[1]/form/div[3]/div/a['+str(page)+']')
            if page == 2:
                if page_2 == True:
                    page_2 = False
                elif page_2 == False:
                    page += 1
                # 다음 페이지로 이동
            page += 1
        except:
            print("이 카테고리는 마무리됨")
            get_page = False
            continue
    print("서로이웃 추가를 종료")

    if neighbors_add != 0:
        try:
            for q in range(neighbors_add):
                driver.switch_to.window(driver.window_handles[-1])
                driver.close()
        except:
            pass
    driver.switch_to.window(driver.window_handles[-1])


print('코드 시작')
login_error = False
while True:  # 네이버 로그인

    try:
        # webdriver_options = webdriver.ChromeOptions()
        # webdriver_options .add_argument('headless')

        # chromedriver = 'C:\stockauto\selenium\chromedriver.exe'
        # driver = webdriver.Chrome(chromedriver, options=webdriver_options)

        driver = webdriver.Chrome(
            'C:\stockauto\selenium\chromedriver.exe')  # 드라이브 크롬으로 설정
        driver.get('https://nid.naver.com/nidlogin.login')  # 네이버 로그인 창으로 이동
        time.sleep(1)  # 1초 대기

        tag_id = driver.find_element_by_name('id')  # id 입력할 곳을 tag_id 변수로 저장
        tag_pw = driver.find_element_by_name('pw')  # pw 입력할 곳을 tag_pw 변수로 저장
        tag_id.clear()  # tag_pw 창에 있는 정보를 지움
        time.sleep(1)  # 1초 대기

        tag_id.click()  # tag_id창 클릭
        pyperclip.copy(str(id))  # id 클립보드에 복사
        tag_id.send_keys(Keys.CONTROL, 'v')  # 붙여넣기
        time.sleep(1)  # 1초 대기

        # pw 입력
        tag_pw.click()  # tag_pw창 클릭
        pyperclip.copy(str(ps))  # pw 클립보드에 복사
        tag_pw.send_keys(Keys.CONTROL, 'v')  # 붙여넣기
        time.sleep(1)  # 1초 대기
        pyperclip.copy('')  # 클립보드 초기화

        # 로그인 버튼을 클릭합니다
        driver.find_element_by_id('log.login').click()  # 로그인 버튼 클릭
        time.sleep(2)  # 2초 대기
        if login_error == False:
            break
    except:
        driver.close()
        login_error = True

print(" [더많은 서로이웃] 로그인 완료")
print("")
neighbors_del()
print(" [더많은 서로이웃] 서로이웃 중에 있는 이웃을 전부 삭제했습니다.")
print("")
date_neighbor_del()
print(" [더많은 서로이웃] 3일간 서로이웃을 받지 않은 신청을 삭제했습니다.")
print("")
txt_count()
print(" [더많은 서로이웃] 오늘 날짜와 카운트 정보 변경 완료")
print("")
add_neighbors()
print(" [더많은 서로이웃] 서로이웃 추가 완료됨")
if count >= 100:
    print(" [더많은 서로이웃] 하루 서로이웃 추가 가능 횟수 초과")
    print(" [더많은 서로이웃] 프로그램을 종료합니다.")
    print("")
    driver.close()
