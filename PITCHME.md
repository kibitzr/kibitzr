# Meet Kibitzr
## Personal Network Assistant
(https://kibitzr.github.io/)

---

## Personal
* Self-hosted - trust no one with your credentials
* Can go wherever you can go (authenticate on websites, ssh, vpn)
* Does what you ask to do, and nothing else

---

## Network
* HTTP requests
* Browser scenarios
* SSH commands (actually any shell code)
* Integrations with Slack, Zapier, MailGun, etc

---

## Assistant
* Define recurrent tasks
* Kibitzr will notify you when something happens

---

## How does it work?
* Kibitzr reads configuration from `kibitzr.yml`
* Executes checks on defined schedule

---

## What is *check*?
1. Fetch content
2. Pass it through sequence of *transforms*
3. Run set of *notifiers* with transformed content

---

# Fetchers

* HTTP with or without Javascript processing
* Bash and Python scripts

+++

## Fetch simple page
Provide an URL, Kibitzr will download

```yaml
checks:
   - url: example.com
```

+++

## Run any shell command
Kibitzr will save it in temporary file and execute with sh

```yaml
checks:
   - script: uptime
```

+++

## Browser Automation
Kibitzr can start Firefox and execute Selenium code (written in Python)

```yaml
checks:
  - name: TeamCity Build
    url: https://teamcity/viewQueued.html?itemId=10270004
    scenario: |
        # Click "guest login" link
        driver.find_element_by_css_selector(
            "form a:nth-child(1)"
        ).click()
    transforms:
      - xpath: //*[@id="buildResults" or contains(@class, 'statusBlock')]//table/tbody/tr[1]/td[2]
      - text
```

---

# Transforms

* XML/HTML selectors, tags stripping
* JSON pretty print, transform with jq
* Plain text processing, like cut, sort
* Compare with previous value

---

# Notifiers

* IMs: Slack, Telegram, gitter
* e-mail: SMTP, Mailgun
* Zapier
* Any bash or Python script

---

# Use cases

* Receive e-mails with credit card balance changes
* Get Slack message on finish of TeamCity task
* Get SMS when production site fails
* Get e-mail on [bug fix] software release

Anything you have to check manually

---

# I want to try!

* Run inside Docker container
* Install on tiniest (free) Amazon Web Service or Google Cloud Platform VM
* Install on your development server
* Install at home

---

# Questions

* Support in Gitter: https://gitter.im/kibitzr/Lobby
* GitHub issues: https://github.com/kibitzr/kibitzr/issues/
