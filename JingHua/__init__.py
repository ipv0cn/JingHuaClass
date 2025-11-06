from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Any
import fake_useragent
import requests
import bs4


class User:
    """
    Response When Error: {
        'msg': 'Message'
    }
    """
    def __init__(self) -> None:
        self.jinghua_url = "http://www.hntyxxh.com"
        self.auth_url = "http://sfrz.ywhnty.com"
        self.openid = ""

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": fake_useragent.UserAgent().random,
        })

    def login(self, username: str, password: str) -> None:
        # 认证系统登录
        login_url = f"{self.auth_url}/cas/login"
        login_data = {
            "username": username,
            "password": password,
            **self._get_login_params()
        }
        self.session.post(login_url, data=login_data)

        # 精华课堂登录
        response = self.session.get(f"{self.jinghua_url}/sso/teacher")
        query_params = parse_qs(urlparse(response.url).query)
        self.session.headers.update({
            "openId": query_params["openid"][0]
        })

    def _get_login_params(self) -> Dict[str, Any]:
        response = self.session.get(f"{self.auth_url}/cas/login")
        soup = bs4.BeautifulSoup(response.text, features="lxml")

        return {
            "lt": soup.find_all(
                "input", {"name": "lt"})[0]["value"],
            "execution": soup.find_all(
                "input", {"name": "execution"})[0]["value"],
            "_eventId": soup.find_all(
                "input", {"name": "_eventId"})[0]["value"],
        }

    def get_course_list(self) -> List[Dict[str, Any]]:
        """
        Response: [
            {
                'id': 114514,
                'name': '大学语文-计应0001',
                'cover': 'https://.../cover.png',
                'teacherName': '张三',
                'avatar': 'https://.../avatar.png',
                'college': '河南信息统计职业学院',
                'code': 'AA001',
                'orgId': 1,
                'imported': 1,
                'department': '大学语文教研室',
                'isLock': 1
            },
            { ... }
        ]
        """
        response = self.session.get(
            f"{self.jinghua_url}/wechat-api/v1/students/courses"
        )
        return response.json()

    def quick_response(self, courseId: int) -> str:
        """
        Response: {
            'msg': '抢答成功！'
        }
        """
        response = self.session.post(
            f"{self.jinghua_url}/wechat-api/v1/responders",
            data={"courseId": courseId}
        )
        return response.text

    def get_user_info(self) -> List[Dict[str, str | int]]:
        """
        Response:[
            {
                'id': 10086,
                'student_id': 1919810,
                'college_id': 1,
                'department_id': 11,
                'class_name': '计应0001',
                'specialty': '计算机应用技术',
                'student_number': '202502000001',
                'comment': '',
                'grade': '2000',
                'tag': '',
                'deleted': 0,
                'org_id': 1,
                'college_name': '河南信息统计职业学院',
                'department_name': '信息技术学院'
            },
            { ... }
        ]
        """
        response = self.session.get(
            f"{self.jinghua_url}/wechat-api/v2/students/role"
        )
        return response.json()

    def get_feedback_list(self) -> List[Dict[str, str | int]]:
        """
        Response: [
            {
                # TODO
            },
            { ... }
        ]
        """
        response = self.session.get(
            f"{self.jinghua_url}/wechat-api/v3/students/orgFeedbacks"
        )
        return response.json()

    def submit_feedback(self, feedbackId: int, comment: str,
                        dimensions: List[int], questions: list[str]
                        ) -> Dict[str, str | List[int | str]]:
        """
        Requests: {
            "comment": "Good", # 意见与建议
            "dimensions": [ # 教学评分
                5, # 教学态度
                5, # 教学内容
                5, # 教学方法
                5, # 教学效果
            ],
            "questions": []
        }
        Response: {}
        """
        response = self.session.post(
            f"{self.jinghua_url}/wechat-api/v3/students/orgFeedbacks"
            f"/{feedbackId}",
            json={
                "comment": comment,
                "dimensions": dimensions,
                "questions": questions
            }
        )
        return response.json()

    def active_sign(self) -> Dict[str, int]:
        """
        Response: {
            "courseId": 770391,
            "signId": 244457,
            "isGPS": 0,
            "isQR": 1
        }
        """
        response = self.session.get(
            f"{self.jinghua_url}/wechat-api/v1/class-attendance/active_sign"
        )
        return response.json()

    def get_message(self) -> List[Dict[str, Any]]:
        """
        Response: [
            {
                "id":"68e60fe361273a293eff9d16",
                "name":"王珏",
                "avatar":"http://.../avatar.png",
                "courseName":"公共英语1-信安2501",
                "title":"关于第一次英语课的通知",
                "content":"...",
                "imgs":[],
                "time":1759907811000,
                "unreadcount":0
            },
            { ... }
        ]
        """
        response = self.session.get(
            f"{self.jinghua_url}/wechat-api/v1/students/notices/noticeSessions"
        )
        return response.json()

    def get_class_question_list(self) -> List[Dict[str, Any]]:
        """
        Response: [
            {
                "courseId": 769887,
                "name": "信息技术与人工智能-信安2501",
                "code": "JF964",
                "cover": "https://.../cover.png",
                "teacherName": "魏旭",
                "libraryId": 769964,
                "questionNum": 0,
                "paperNum": 0,
                "openNum": 0
            },
            { ... }
        ]
        """
        response = self.session.get(
            f"{self.jinghua_url}/wechat-api/v3/students/courses"
        )
        return response.json()

    def get_question_list(self, courseId: int, isOpen: bool = True,
                          page: int = 0) -> Dict[str, Any]:
        """
        Response: {
            "questionNum":3,
            "paperNum":0,
            "questions": [
                {
                    "id":1762878,
                    "code":"T0002-1-1-1-1-1",
                    "type":4,
                    "difficulty":1,
                    "isObjective":1,
                    "content":"...",
                    "status":1,
                    "answerOpen":0,
                    "onTime":0,
                    "timingClose":null,
                    "lastOpenTime":"2025-11-06T02:09:11.000Z",
                    "isAnswered":1,
                    "isCorrect":1
                },
                { ... }
            ]
        }
        """
        response = self.session.get(
            f"{self.jinghua_url}/wechat-api/v3/students/questions",
            params={
                "courseId": courseId,
                "isOpen": int(isOpen),
                "page": page
            }
        )
        return response.json()

    def get_question_info(self, questionId: int) -> Dict[str, Any]:
        """
        Response: {
            "id":1762878,
            "code":"T0002-1-1-1-1-1",
            "content":"...",
            "type":4,
            "difficulty":1,
            "isObjective":1,
            "blankNum":3,
            "minChosen":null,
            "maxChosen":null,
            "status":1,
            "answerOpen":0,
            "reviewOpen":0,
            "onTime":0,
            "timingClose":null,
            "lastOpenTime":"2025-11-06T02:09:11.000Z",
            "isAnswered":1,
            "isSet":0,
            "summary":"",
            "answerContent":[],
            "answer":
                [{"rank":0,"answer":"that"},
                {"rank":1,"answer":"whose"},
                {"rank":2,"answer":"mine"}],
            "review":""
        }
        """
        response = self.session.get(
            f"{self.jinghua_url}/wechat-api/v3/students/questions"
            f"/{questionId}",
        )
        return response.json()
