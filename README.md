### <u>Hướng dẫn chạy phần lõi đề tài</u>

---

1. API gửi tới server để server cấp id cho có dạng:

- api có dạng: https://localhost:8080/putOptions

```
{
    "mac":"1234"
}
```

---

2. API để lưu file cho phép đẩy file lên, trả về text và ID, thêm mức độ để xử lý file đẩy lên, (deskew, deblur, autofill, xử lý bảng,(lưu file và text cùng thư mục temp)

- ex:
  https://localhost:8080/recieveFile/?id=0db1169f-f30d-11e9-bf41-049226165991&mac=1234&skew=true&blur=false&basic=false&advance=false&filetype=pdf&filename=dan

---

3.API nhận text và ID, đẩy lên elastic search.

- api có dạng: localhost:8080//pushtextandid

```
{
    "mac":"123456sodp",
    "id":"1",
    "contents":"noi dung cua file"
}
```
---
4.  API gửi lên đoạn text, trả về danh sách các tên file, nội dung của file được giới hạn 100 từ và ID đi kèm

- api có dạng:localhost:8080//search
- json send:

```
{
    "mac":"documents",
    "search_contents":"khong co viec gi kho"
}
```

- json recieve:

```
[
    {
        "_source": {
            "id": "1",
            "contents": "khong co",
            "filename": "test.txt"
            }
    },
    {
        "_source": {
            "id": "2",
            "contents": "không có việc gì khó chỉ sợ lòng không bền",
            "filename": "temp.txt"
        }
    }
]
```
---
5. API nhận ID, chỉ trả về file text

- api: https://localhost:8080/getAllContents
- json client tải lên có dạng:

```
   {
       "id":"1",
       "mac":"1234"
   }
```
---
6. trước tiên phải gọi tới Api con trả về extension của file gốc

- api có dạng: localhost:8080/getRootFileExtension
- json client tải lên có dạng:

```
   {
       "id":"1",
       "mac":"1234"
   }
```
---
7. API Download nhận id từ client và trả file gốc về:

- api have format: localhost:8080/download
- json client send have format:

```
    {
        "mac": "1234",
        "id": "123"
    }
```
