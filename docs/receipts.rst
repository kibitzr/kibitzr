========
Receipts
========

.. highlight: yaml

TeamCity build status change
    
.. code-block:: 

    pages:
	  - name: TeamCity Build
	    template: teamcity-build
	    url: https://teamcity/viewQueued.html?itemId=10270004

    templates:
        teamcity-build:
            xpath: //*[@id="buildResults" or contains(@class, 'statusBlock')]//table/tbody/tr[1]/td[2]
            format: text
            period: 30
            scenario: teamcity-login

    scenarios:
        teamcity-login: |
            from selenium.common.exceptions import NoSuchElementException
            try:
                driver.find_element_by_css_selector(
                    "#pageContent > form > table > tbody > tr:nth-child(4) > td > span > a:nth-child(1)"
                ).click()
                driver.implicitly_wait(60)
            except NoSuchElementException:
                # Second time session will be already authorized
                pass



BitBucket pull request ready to merge

.. code-block:: 
    pages:
	  - name: PR ready to merge
	    template: bitbucket-pr-ready
	    url: https://bitbucket.ncbi.nlm.nih.gov/projects/PMC/repos/granthub-service/pull-requests/307/overview

    templates:
        bitbucket-pr-ready:
            xpath: //*[@class="plugin-section-primary"]
            format: text
            period: 30
            delay: 5
            scenario: bitbucket-login

    scenarios:
        bitbucket-login: |
            from selenium.common.exceptions import NoSuchElementException
            try:
                driver.find_element_by_id("j_username").send_keys("username")
                driver.find_element_by_id("j_password").send_keys("password")
                driver.find_element_by_id("submit").click()
            except NoSuchElementException:
                # Second time session will be already authorized
                pass


Mailgun notifications configuration

.. code-block:: 
    notifiers:
        mailgun:
            key: key-asdkljdiytjk89038247102384
            domain: sandbox57895483457894350345.mailgun.org
            to: John Doe <john.doe@gmail.com>
