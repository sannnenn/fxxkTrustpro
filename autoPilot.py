from time import sleep
from configparser import SafeConfigParser

from selenium import webdriver #webdriver本体
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.alert import Alert

class autoPilot:
    #ドライバー
    _driver = None
    #待機時間設定
    _wait = None
    #trustproログインページ
    _URL = ""
    #ユーザ情報
    _uid = ""
    _upw = ""

    #週予定
    _startWeekDay = ""
    

    #デフォルトコンストラクタ
    def __init__(self):
        #設定情報取得
        iniFile = SafeConfigParser()
        iniFile.read("./fxxkTrustpro.ini")
        self._URL = iniFile.get("Settings", "URL")
        self._uid = iniFile.get("User", "userID")
        self._upw = iniFile.get("User", "userPW")

        #週予定取得
        weeklyReportFile = SafeConfigParser()
        weeklyReportFile.read("./weeklyReport.txt")
        self._startWeekDay = weeklyReportFile.get("Settings", "startDate")

        #chorome起動
        self._driver = webdriver.Chrome("./chromedriver.exe") 
        #待ち時間設定
        self._wait = WebDriverWait(self._driver, 20)

    #ログインする
    def login(self):
        #trustproのログインページに移動
        self._driver.get(self._URL) 
        
        #ログイン情報入力
        userid = self._driver.find_element_by_css_selector("#userid").send_keys(self._uid)
        userpw = self._driver.find_element_by_name("password").send_keys(self._upw)
        
        #ログインボタンを押す
        self._driver.find_element_by_xpath("/html/body/div/div[1]/div/form/div[5]/div/button").click()
        
        #表示待ち
        self._wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "btn_size_07")))


    #指定した開始日の週予定を開く
    def openWeeklyReport(self):
        #週報に移動する
        self._driver.find_element_by_id("name2").click()
        
        #表示待ち
        self._wait.until(expected_conditions.element_to_be_clickable((By.ID, "_LO_DEF_SEARCH_BTN")))

        #目的の週計画を探す
        for tag in self._driver.find_elements_by_name("form.shuu_kaishibi"):
            tagValue = tag.get_attribute("value")
            #目的の週だった場合インデックスを取得する
            if tagValue == self._startWeekDay:
                targetIndex = tag.get_attribute(By.ID)[-1]
                break
        
        #週報クリック
        self._driver.find_element_by_id("keikaku_status" + str(targetIndex) + "_VIEW_LABEL").click()

        #表示待ち
        self._wait.until(expected_conditions.element_to_be_clickable((By.ID, "nippou_keikaku_view_kinmu_date0_VIEW_LABEL")))
        
    def setWeekReport(self):

        weeklyReportFile = SafeConfigParser()
        weeklyReportFile.read("./weeklyReport.txt")
        
        for i in range(5):
            #休日の場合は処理はしない(曜日のところが赤くなってる)
            if weeklyReportFile.get(str(i), "isHoliday") == "1" or self._driver.find_element_by_id("nippou_keikaku_view_youbi" + str(i) + "_VIEW_LABEL").get_attribute("style").strip() != "":
                continue

            #週計画取得
            department = weeklyReportFile.get(str(i), "departmentNameNumber")
            project = weeklyReportFile.get(str(i), "projectNameNumber")
            process = weeklyReportFile.get(str(i), "process")
            hour = weeklyReportFile.get(str(i), "hour")
            min = weeklyReportFile.get(str(i), "min")
            remarks = weeklyReportFile.get(str(i), "remarks")

            #曜日ごとの計画に移動
            self._wait.until(expected_conditions.element_to_be_clickable((By.ID, "nippou_keikaku_view_kinmu_date" + str(i) + "_VIEW_LABEL")))
            self._driver.find_element_by_id("nippou_keikaku_view_kinmu_date" + str(i) + "_VIEW_LABEL").click()

            #勤務計画保存ボタンが表示されるまで待つ
            sleep(5)

            #追加ボタン押下
            self._wait.until(expected_conditions.element_to_be_clickable((By.ID, "addLineBtn")))
            self._driver.find_element_by_id("addLineBtn").click()

            sleep(4)
            self._wait.until(expected_conditions.element_to_be_selected)
            departmentSelect = Select(self._driver.find_element_by_id("sagyou_keikaku_view_bumon_name_view0"))
            departmentSelect.select_by_value(department)
            sleep(1)

            projectSelect = Select(self._driver.find_element_by_id("sagyou_keikaku_view_project_name_view0"))
            projectSelect.select_by_value(project)
            sleep(1)

            processSelect = Select(self._driver.find_element_by_id("sagyou_keikaku_view_pj_koutei_view0"))
            processSelect.select_by_value(process)
            sleep(1)

            hourSelect = Select(self._driver.find_element_by_id("sagyou_keikaku_view_sagyou_time_hour_view0"))
            hourSelect.select_by_value(hour)
            minSelect = Select(self._driver.find_element_by_id("sagyou_keikaku_view_sagyou_time_min_view0"))
            minSelect.select_by_value(min)
            sleep(2)

            self._driver.find_element_by_id("sagyou_keikaku_view_text_bikou0").send_keys(remarks)

            #計画保存
            self._driver.find_element_by_xpath("/html/body/div/div/div[4]/div/div[1]/div[4]/div[1]/div/div/div[1]/div[3]/form/div[1]/div[2]/div[2]/input").click()
            Alert(self._driver).accept()
            sleep(8)

        #申請
        self._driver.find_element_by_xpath("/html/body/div/div/div[4]/div/div[1]/div[3]/form/div[1]/div[2]/div[2]/input").click()
        sleep(3)






