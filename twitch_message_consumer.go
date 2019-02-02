/*
    TODO:
    Pull pass from .oauth file
    add Args
*/

package main

import (
	"github.com/thoj/go-ircevent"
    "github.com/segmentio/kafka-go"
	"fmt"
    "context"
    "encoding/json"
    s "strings"
)

const channel = "#jonthomask";
const serverssl = "irc.twitch.tv:6667"
const pass = "" // temp removed

type TwitchSchema struct {
    Channel string `json:"channel"`
    Username string `json:"username"`
    Message string `json:"message"`
}

func main() {

    w := kafka.NewWriter(kafka.WriterConfig{
    	Brokers: []string{"localhost:9092"},
    	Topic:   "twitch-messages",
    	Balancer: &kafka.LeastBytes{},
    })

    ircnick1 := "talis_jtk"
    irccon := irc.IRC(ircnick1, "Talis_JTK")
    irccon.Debug = true
    irccon.Password = pass

    // welcome message
    irccon.AddCallback("001", func(e *irc.Event) {
        irccon.Join(channel)
    })

    // joined channel
    irccon.AddCallback("366", func(e *irc.Event) {
        fmt.Printf("Joined %s\n", channel)
    })

    irccon.AddCallback("PRIVMSG", func(e *irc.Event) {
        channel_clean := s.Replace(e.Arguments[0], "#", "", -1)
        data := &TwitchSchema{Channel: channel_clean, Username: e.Nick, Message: e.Message()}
        data_json, err := json.Marshal(data)
        fmt.Println(string(data_json))

        if err != nil {
            fmt.Println(err)
            return
        }

        w.WriteMessages(context.Background(),
        	kafka.Message{
        		Value: []byte(string(data_json)),
        	},
        )
    });

    err := irccon.Connect(serverssl)

	if err != nil {
		fmt.Printf("Err %s", err )
		return
	}

    irccon.Loop()
}
