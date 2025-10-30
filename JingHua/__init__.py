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
                        ) -> Dict[None, None]:
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
