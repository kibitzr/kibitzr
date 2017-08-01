=======
Recipes
=======


GitHub API release notification
-------------------------------

.. code-block:: yaml

    checks:
      - name: Kibitzr GitHub release
        url: https://api.github.com/repos/kibitzr/kibitzr/releases/latest
        transform:
          - jq: .tag_name + " " + .name
          - changes: verbose
        notify:
          - slack

Example message:

    | **Kibitzr**
    | Previous value:
    | v2.6.6 Added batch syntax to configuration file
    | New value:
    | v2.6.7 Invoke jq with --raw-output


Wordpress Plugin update (featuring batch syntax)
------------------------------------------------

.. code-block:: yaml

    checks:
      - batch: "Wordpress plugin {0} updates"
        transform:
            - xpath: '//*[@id="changelog"]/h4[1]'
            - text
            - changes: verbose
        notify:
            - slack
        period: 3600
        url-pattern: "https://wordpress.org/plugins/{0}/"
        items:
          - advanced-custom-fields
          - akismet
          - better-wp-security
          - black-studio-tinymce-widget
          - contact-form-7
          - disable-comments
          - duplicate-post


Travis CI build status
----------------------

.. code-block:: yaml

    checks:
      - name: Kibitzr Build Status
        url: https://travis-ci.org/kibitzr/kibitzr
        transform:
          - css: div.build-info > h3
          - text
          - changes
        delay: 1
        period: 600
        notify:
          - slack

TeamCity build status change
----------------------------

.. code-block:: yaml

    checks:
      - name: TeamCity Build
        template: teamcity-build
        url: https://teamcity/viewQueued.html?itemId=10270004

    templates:
      teamcity-build:
        form:
          - xpath: '//*[@id="pageContent"]/form/table/tbody/tr[4]/td/span/a[1]'
            click: true
        delay: 3
        transform:
          - xpath: //*[@id="buildResults" or contains(@class, "statusBlock")]//table/tbody/tr[1]/td[2]
          - text
          - jinja: "{{ lines | join(' ') }}"
          - changes: new
        period: 30 seconds


BitBucket pull request ready to merge
-------------------------------------

.. code-block:: yaml

    checks:
      - name: PR ready to merge
        template: bitbucket-pr-ready
        url: https://bitbucket/repos/kibitzr/pull-requests/307/overview

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
