package main

import (
	"github.com/gin-gonic/gin"
)

const (
	IMAGEPATH = "../images/"
)

func main() {

	router := gin.Default()

	// 根据 image_id 查找图片
	router.Static("/images", "../images")

	// 上传图片
	router.POST("/upload", upload_image)

	// 搜索相似图片
	router.POST("/search", search_image)

	router.Run(":7777")
}
