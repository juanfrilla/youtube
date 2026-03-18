package main

import (
	"fmt"
	"log"
	"os"
	"time"

	"github.com/playwright-community/playwright-go"
)

func run() {
	os.Setenv("SELENIUM_REMOTE_URL", "http://localhost:4444")
	pw, err := playwright.Run()
	if err != nil {
		log.Fatalf("Error starting Playwright: %v", err)
	}
	defer pw.Stop()

	browser, err := pw.Chromium.Launch(playwright.BrowserTypeLaunchOptions{
		Headless: playwright.Bool(false),
		Args:     []string{"--start-maximized"},
		Channel:  playwright.String("chrome"),
	})
	if err != nil {
		log.Fatalf("Error running browser: %v", err)
	}
	defer browser.Close()

	var page playwright.Page
	var context playwright.BrowserContext
	contexts := browser.Contexts()

	if len(contexts) == 0 {
		var err error
		context, err = browser.NewContext(playwright.BrowserNewContextOptions{
			NoViewport: playwright.Bool(true),
		})
		if err != nil {
			log.Fatalf("Error creating context: %v", err)
		}
	} else {
		context = contexts[0]
	}
	defer context.Close()

	pages := context.Pages()
	if len(pages) > 0 {
		page = pages[0]
	} else {
		var err error
		page, err = context.NewPage()
		if err != nil {
			log.Fatalf("Error creating page: %v", err)
		}
	}
	defer page.Close()

	fmt.Println("🌍 Navigating straight to stackoverflow.com...")
	_, err = page.Goto("https://stackoverflow.com/", playwright.PageGotoOptions{
		WaitUntil: playwright.WaitUntilStateDomcontentloaded,
	})
	if err != nil {
		log.Fatalf("Error in navigation: %v", err)
	}
	sleepTime := 2

	fmt.Printf("⏳ Waiting %d seconds before closing...\n", sleepTime)
	time.Sleep(time.Duration(sleepTime) * time.Second)
}

func main() {
	run()
}

// step 1: go run github.com/playwright-community/playwright-go/cmd/playwright@latest install --with-deps
