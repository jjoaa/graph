# 의료용 마약류 통계 대시보드
<br />  

## 1. 소개
> 의료용 마약류 오남용에 관해 파악하기 위해 KOSIS의 의료용마약류취급현황 통계자료를 사용하였습니다 \
> 이 프로젝트는 크게 세가지 부분을 확인하고자 하였습니다.
 - 여성과 남성 중에 어느 성별이 더 의료용 마약류를 처방받는지
 - 어느 연령대가 의료용 마약류를 가장 많이 처방 받았는지
 - 각 효능별로 어떤 성분이 많이 처방되는지 

<br /> <br />
![Image](https://github.com/user-attachments/assets/48c7f579-4990-4bfc-a87a-31420fc91822)
<br /> <br />

### 작업기간
2025/04, 1주
<br /><br />

### 인력구성
1인
<br /><br /><br />

## 2. 기술스택

<img alt="Python" src ="https://img.shields.io/badge/Python-3776AB.svg?&style=for-the-badge&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/html-E34F26?style=for-the-badge&logo=html5&logoColor=white">  <br /><br /> 

## 3. 기능
### 📂 Project Structure (폴더 구조)
```
Graph_Drug/
|     
|ㅡ templates /  
|  |ㅡ index.html       # 메인 페이지    
|  |ㅡ pie_chart.html   # 성분별 파이그래프, 약물 처방량과 환자수 산점도 
|ㅡ app.py              # 각 그래프 처리
|ㅡ static /            # 성별 그래프 img
└── README.md           # GitHub 설명 파일
```
<br /><br /><br />

## 4. 상세페이지 
- **연도별 효능별 처방량**
  
  ![Image](https://github.com/user-attachments/assets/cfe02b25-a977-4a40-aa13-dcbb399c75db)
<br />

- **성분별 파이그래프, 처방량과 환자수 산점도**

![Image](https://github.com/user-attachments/assets/258f07b7-6f07-4a71-92cc-62f62c6847bf)
<br />

- **연령대별 성별 환자수 및 처방량**

![Image](https://github.com/user-attachments/assets/a7423600-9407-4607-8025-fbdbc775f980)
<br />  



<br /><br /> <br /> <br /> 


## 5. 분석 결과 
 - **여성과 남성 중에 어느 성별이 더 의료용 마약류를 처방받는지**<br />
   10대 이하는 남성이, 그 이후부터는 여성이 의료용 마약류를 더 많이 처방받음을 확인함
    
 - **어느 연령대가 의료용 마약류를 가장 많이 처방 받았는지**<br />
    2019년 50대 / 
    2020년 40대 /
    2021, 2022, 2023년 60대
 
 - **각 효능별로 어떤 성분이 많이 처방되는지** <br />
   항불안제 : 알프라졸람 <br />
   최면진정제 : 졸피뎀 <br />
   진통제 : 옥시코돈 <br />
   식욕억제제 : 펜디메트라진 <br />
   마취제 : 프로포폴 <br />
   
   
<br /><br /> <br /> 

## 6. 앞으로 학습할 것들, 나아갈 방향
- csv 파일이 아닌 OPEN API 연동
<br /><br /> <br /> 
