# 카페조아 | cafejoa - 카페에 답이 있다.



## 🎉프로젝트 소개

본인의 감성과 생활을 사람들에게 공유하세요! 

카페를 좋아하는 사람들이 모여 카페 정보와 카페에서 듣고 싶은 노래를 공유하고 싶어 만들게 되었습니다.



[카페조아](http://moveuk.shop/login?msg=%EB%A1%9C%EA%B7%B8%EC%9D%B8+%EC%A0%95%EB%B3%B4%EA%B0%80+%EC%A1%B4%EC%9E%AC%ED%95%98%EC%A7%80+%EC%95%8A%EC%8A%B5%EB%8B%88%EB%8B%A4.)



## 🥰프로젝트 화면

![main](https://user-images.githubusercontent.com/84966961/179533633-087b4240-65ea-4f9a-a7e7-da9c16fb3a56.gif)



## 📸시연 영상

소리가 없으니 감안해주시면 감사드립니다. 🤡





## 🧑‍💻 제작 기간 & 팀원 소개

- 2022년 7월 11일 ~ 2022년 7월 14일

- 팀원
  
  - 이광훈
  
  - 이동욱 - [GitHub](https://github.com/Moveuk?tab=repositories) [dev blog](https://dul2.tistory.com/)
  
  - 이석준



## 🔨사용 기술

- Server: AWS EC2 (Ubuntu 18.04 LTS)

- Framework: Flask (Python)

- Database: MongoDB

- View : HTML5, CSS3(+ Bulma framework), Javascript + jinja2(template engine)

- Design Tool (Figma)

- Tool : Git, Notion, Slack





## 💡 프로젝트를 하며 얻은 것!

### Server-Side Rendering (SSR) vs Client-Side Rendering (CSR)

- 서버사이드렌더링에 대하여 jinja2 템플릿 엔진을 통해 공부하는 기회였다.

- 요약 - 한번에 그려서 보내기에 클라이언트 측에서 빠르며, SEO에 강점이 있다.

### JWT

- 세션 / 쿠키 방식보다 개선된 로그인, 회원 가입 방식에 대해서 이해하고 배우는 기회였다.

### Python, MongoDB 등의 새로운 기술

- 기존에 프로젝트를 구현할 때 사용하지 않았었던 새로운 기술들을 접했다. 특히 MongoDB의 유연성에 놀랐다.
  
  

더 디테일한 회고는 각 팀원별 블로그를 참조해 주시면 감사드립니다 :) 



## ✨핵심 기능 소개

1. 로그인, 회원가입
   
   - JWT를 이용한 로그인과 회원가입을 구현하였으며, 서비스를 이용하려면 로그인이 필요하도록 구성하였습니다.
     
     ![signin](https://user-images.githubusercontent.com/84966961/179533253-74f65c66-b07e-4978-8b51-93c6d2151e4a.gif)
   
   - 회원 가입시 중복 확인 기능 및 정규식을 이용하여 아이디와 비밀번호가 최소 조건 만족에 만족해야 가입이 되도록 기능을 구현하였습니다. 
     
     ![join](https://user-images.githubusercontent.com/84966961/179533403-648f8955-0875-41f8-9522-e0408d938454.gif)
     
     

2.  마이 페이지 기능
   
   - 본인 이름과 프로필 사진 수정이 가능합니다.
     
     ![change_profile](https://user-images.githubusercontent.com/84966961/179533991-8a6ef927-6307-4a6b-8f53-59113237460c.gif)
     
     

3.  카페 후기글 CRUD 기능
   
   - modal 창을 이용하여 사용자들의 게시글을 확인할 수 있도록 했습니다.
     
     ![post_modal](https://user-images.githubusercontent.com/84966961/179534550-a9474f7b-6b31-40dc-97fc-88e887958b15.gif)
   
   - 사용자가 카페의 사진과 더불어 정보를 입력한 후 글을 포스팅하고, 추후 수정 혹은 삭제가 가능합니다.
     
     ![edit_post](https://user-images.githubusercontent.com/84966961/179535636-2e2e6a1d-77f1-4ef0-9af8-2193d9132111.gif)
     
     ![delete_post](https://user-images.githubusercontent.com/84966961/179536864-c08b45fb-f081-444d-ab64-238dc7b6d007.gif)
     
     

4. 좋아요 ❤️ 기능
   
   - Ajax 비동기 처리를 통하여 좋아요 ❤️ 수를 확인할 수 있습니다.
     
     ![like](https://user-images.githubusercontent.com/84966961/179534760-72ca0336-4a33-45b6-a1b8-0ced1cd6ee41.gif)
     
     

5. 유튜브 영상 - 카페에서 듣고 싶은 노래 추천하기 기능
   
   - 유튜브 영상을 url을 통해 포스팅 가능합니다.
     
     ![youtube](https://user-images.githubusercontent.com/84966961/179536179-0429e398-d89c-4c53-8439-6ae81a961481.gif)
   
   
