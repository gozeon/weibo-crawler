package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
	"gopkg.in/mgo.v2/bson"

	"gopkg.in/mgo.v2"
)

var MONGO_URL string

type Weibo struct {
	Id        bson.ObjectId `json:"_id,omitempty" bson:"_id,omitempty"`
	UserId    int32         `json:"user_id" bson:"user_id"`
	WeiboId   int64         `json:"id" bson:"id"`
	Bid       string        `json:"bid" bson:"bid"`
	Text      string        `json:"text" bson:"text"`
	TextLink  string        `json:"text_link" bson:"text_link"`
	Pics      string        `json:"pics" bson:"pics"`
	CreatedAt string        `json:"created_at" bson:"created_at"`
}

func getWeibo(w http.ResponseWriter, r *http.Request) {
	w.Header().Add("Content-Type", "application/json")
	date := mux.Vars(r)["date"]

	var err error

	client, err := mgo.Dial(MONGO_URL)
	if err != nil {
		log.Fatalln(err.Error())
	}
	weiboCollection := client.DB("weibo").C("weibo")
	var weibos []Weibo

	err = weiboCollection.Find(bson.M{
		"created_at": date,
		"text_link": bson.RegEx{
			`\S`,
			"",
		},
	}).All(&weibos)
	//err = weiboCollection.Find(bson.M{}).All(&weibos)
	if err != nil {
		log.Fatal(err.Error())
	}
	json.NewEncoder(w).Encode(weibos)
}

func init() {
	MONGO_URL = os.Getenv("MONGO_URL")

	if MONGO_URL == "" {
		MONGO_URL = "mongodb://localhost:27017/"
	}

	fmt.Println("mongdb url: " + MONGO_URL)
}

func main() {
	router := mux.NewRouter()
	router.HandleFunc("/weibo/{date:[0-9]{4}-[0-9]{2}-[0-9]{2}}", getWeibo).Queries("type", "json").Methods("GET")
	err := http.ListenAndServe(":7897", router)
	if err != nil {
		log.Fatal(err.Error())
	}
}
