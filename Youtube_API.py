import googleapiclient.discovery  # YouTube Data API library
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from textblob import TextBlob ; # Thư viện cảm xúc

# Xây dựng ứng dụng Search Youtube 
class SearchAPI:
    def __init__(self,KEY_API):  
        self.KEY_API = KEY_API 

        # Khỏi tạo của sổ 
        # Initialize the Tkinter window
        self.root = tk.Tk()
        self.root.title("Search YouTube API")
        self.root.configure(bg='lightblue') # Mầu nền cho của sỗ chinb 

        # Tạo textbox để nhập vào key_vodeo
        tk.Label(self.root, text="Mã Video: (Video ID):").grid(row=0, column=0, padx=10, pady=10)
        self.entry_video_id = tk.Entry(self.root, width=40) 
        self.entry_video_id.grid(row=0, column=1, padx=10, pady=10) 
        # Tạo nút bấm  
        # Create a button with specified options 
        self.button = tk.Button(self.root,
                        text="Click Me!",   # Lable of button  
                        command=self.click_button,  
                        bg="lightgray", 
                        fg="black",
                        font=("Arial", 12), 
                        height=2, 
                        width=15,)
        self.button.grid(row=0, column=2, padx=10, pady=10) 
        #  Tạo listbox lựa chọn phân loại bình luận 
        # Label text for title
        tk.Label(self.root, text="Lựa chọn bình luận : ",    # Bị lỗi 
                       font = ("Times New Roman", 10)).grid(column=0, 
                        row=3, padx=10, pady=25)   
        # combobox creation  
        self.comments_type = tk.StringVar()  
        self.combo_comments = ttk.Combobox(self.root, width=20, textvariable = self.comments_type)

        # Thêm thành phần vào combobox 
        self.combo_comments["values"] =  ("All",     #  tất cả bình luận 
                                   "Positive",  # Bình luần tích cực 
                                   "Nagative")  #  Bình  luận tiêu cực 
        self.combo_comments.grid(column=1, row=3) 
        self.combo_comments.current(0)   # mặt  định sử dụng ALL

        # Nút áp dụng lọc 
        self.filter_button = tk.Button(self.root, 
                                       text="Ap dụng lọc", 
                                       command=self.apply_filter, 
                                       bg="lightblue", 
                                       font=("Arial", 10)) 
        self.filter_button.grid(row=3, column=2, padx=10, pady=10)

        # Tạo bản hiển thị bình luận    // Tên các cột gồm :  Số thứ tự, bình luận , lược yêu thích
        self.table = ttk.Treeview(self.root, columns=("STT", "Comment", "Likes"), show="headings")
        self.table.heading("STT", text="Số thứ tự")
        self.table.heading("Comment", text="Bình Luận")
        self.table.heading("Likes" , text="Yêu Thích")

        # Đặt độ rộng  củ cột   Điều chỉnh kích thước của cột
        self.table.column("STT", width=70, anchor="center")
        self.table.column("Comment", width=600, anchor='w')
        self.table.column("Likes", width=100, anchor="center")   # Thêm mới
        self.table.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        # Chạy vòng lập chính
        self.root.mainloop() 
    # Hàm xử lý hành động lựa chọn select box
    def analyze_sentiment(self, text) : 
        analysis = TextBlob(text) 
        # Chuyển đổi các thành phần 
        if analysis.sentiment.polarity > 0.1: 
            return "Positive" 
        elif analysis.sentiment.polarity < -0.1 : 
            return "Nagative" 
        else : 
            return "Neutral" 
    # Ap dụng bộ lọc 
    def apply_filter(self) : 
        if not self.all_comments :   
            messagebox.showwarning("Không có bình  luận nào để lọc")
            return
        selected_filter = self.comments_type.get() 
        if selected_filter == "All"  : 
            filtered_comments = self.all_comments
        else : 
            filtered_comments = [(text, likes, sentiment) for text, likes, sentiment in self.all_comments 
                                 if sentiment == selected_filter]
        self.display_comments(filtered_comments)


    # Xử lý xự kiện từ nút bấm
    def click_button(self) : 
        video_id = self.entry_video_id.get().strip()  # Truy vấn mã video 
        if not video_id:
            messagebox.showwarning("Cảnh Báo", "Vui lòng nhập mã video!")
            return
        # Lấy bình luận từ Youtube API 
        comments = self.get_youtube_comments(self.KEY_API, video_id)
        if not comments:
            messagebox.showinfo("Thông báo", "Không tim thấy bình luận từ video hoặc gặt lỗi")
            return
        # Lua tất cả các bình luận và phân tích cảm xúc 
        self.all_comments = [] 
        for comment_text, like_count in comments: 
            sentiment = self.analyze_sentiment(comment_text) 
            self.all_comments.append((comment_text, like_count, sentiment))
        
        # Hiển thị bình luận  trong bảng
        self.display_comments(self.all_comments)
    # Viết hàm đễ hiển thị bình luận trong bảng 
    def display_comments(self, comments) : 
        # Xóa old data in table 
        for row in self.table.get_children():  
            self.table.delete(row) 

        # Thêm  dữ liệu vào bảng
        for stt, (comment_text, like_count, sentiment) in  enumerate(comments, start=1): 
            self.table.insert("", "end", values=(stt, comment_text, like_count, sentiment))

 
    #$ Lấy bình luận từ youtube APi 
    def get_youtube_comments(self, api_key, video_id):
        try:
            # Build the YouTube API service
            youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)
            # Fetch comments
            comments = []
            next_page_token = None

            while True:
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    pageToken=next_page_token,
                    textFormat="plainText",
                    maxResults=100  # Maximum comments per API call\
                )
                response = request.execute()

                # Extract comments from response
                for item in response["items"]:
                    comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    like_count = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
                    comments.append((comment_text, like_count))  #  Append với dạng tuple

                # Check if there’s a next page
                next_page_token = response.get("nextPageToken")
                if not next_page_token:
                    break
            return comments
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi bình luận: {str(e)}")
            return []  
#  Chạy ứng dụng 
if __name__ == "__main__" : 
    API_KEY = "AIzaSyC15x3HDn8ffAfyrfohUu8qKPaNNYJRviU"  
    app = SearchAPI(API_KEY)