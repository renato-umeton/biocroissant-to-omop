::: {#MathJax_Message style="display: none;"}
:::

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: {.container-fluid .main-container}
::::::: {.navbar .navbar-default .navbar-fixed-top role="navigation"}
:::::: container
:::: {.navbar-header .active}
[]{.icon-bar} []{.icon-bar} []{.icon-bar}

[](https://ohdsi.github.io/CommonDataModel/index.html){.navbar-brand}

::: {}
![](OMOP%20Common%20Data%20Model_files/ohdsi16x16.png) OMOP Common Data
Model
:::
::::

::: {#navbar .navbar-collapse .collapse}
- [[]{.fa
  .fa-house}](https://ohdsi.github.io/CommonDataModel/index.html)
- [[]{.fa .fa-landmark} Background []{.caret}](#){.dropdown-toggle
  toggle="dropdown" role="button" bs-toggle="dropdown"
  aria-expanded="false"}
  - [Model
    Background](https://ohdsi.github.io/CommonDataModel/background.html)
  - [CDM Refresh
    Process](https://ohdsi.github.io/CommonDataModel/cdmRefreshProcess.html)
  - [How the Vocabulary is
    Built](https://ohdsi.github.io/CommonDataModel/vocabulary.html)
- [[]{.fa .fa-list-alt} Conventions []{.caret}](#){.dropdown-toggle
  toggle="dropdown" role="button" bs-toggle="dropdown"
  aria-expanded="false"}
  - [THEMIS Convention Library](https://ohdsi.github.io/Themis)
  - [General
    Conventions](https://ohdsi.github.io/CommonDataModel/dataModelConventions.html)
  - [Patient Privacy and
    OMOP](https://ohdsi.github.io/CommonDataModel/cdmPrivacy.html)
  - [Custom
    Concepts](https://ohdsi.github.io/CommonDataModel/customConcepts.html)
- [[]{.fa .fa-history} CDM Versions []{.caret}](#){.dropdown-toggle
  toggle="dropdown" role="button" bs-toggle="dropdown"
  aria-expanded="false"}
  - [CDM v3.0](https://ohdsi.github.io/CommonDataModel/cdm30.html)
  - [CDM v5.3](https://ohdsi.github.io/CommonDataModel/cdm53.html)
  - [CDM v5.4](#){.dropdown-toggle toggle="dropdown" role="button"
    bs-toggle="dropdown" aria-expanded="false"}
    - [CDM v5.4](https://ohdsi.github.io/CommonDataModel/cdm54.html)
    - [Changes from CDM
      v5.3](https://ohdsi.github.io/CommonDataModel/cdm54Changes.html)
    - [Entity
      Relationships](https://ohdsi.github.io/CommonDataModel/cdm54erd.html)
    - [Detailed tooling support per CDM
      field](https://ohdsi.github.io/CommonDataModel/cdm54ToolingSupport.html)
- [[]{.fa .fa-plus-square} CDM Additions []{.caret}](#){.dropdown-toggle
  toggle="dropdown" role="button" bs-toggle="dropdown"
  aria-expanded="false"}
  - [Types of CDM
    Additions](https://ohdsi.github.io/CommonDataModel/typesOfAdditions.html)
  - [How to Propose Changes to the
    CDM](https://ohdsi.github.io/CommonDataModel/cdmRequestProcess.html)
  - [Accepted Changes](#){.dropdown-toggle toggle="dropdown"
    role="button" bs-toggle="dropdown" aria-expanded="false"}
    - [CDM version in
      development](https://github.com/OHDSI/CommonDataModel/tree/develop)
- [[]{.fa .fa-question} How to []{.caret}](#){.dropdown-toggle
  toggle="dropdown" role="button" bs-toggle="dropdown"
  aria-expanded="false"}
  - [Download the
    DDL](https://ohdsi.github.io/CommonDataModel/download.html)
  - [Use the CDM R
    Package](https://ohdsi.github.io/CommonDataModel/cdmRPackage.html)
  - [Calculate Drug
    Dose](https://ohdsi.github.io/CommonDataModel/drug_dose.html)
- [[]{.fa .fa-life-ring} Support []{.caret}](#){.dropdown-toggle
  toggle="dropdown" role="button" bs-toggle="dropdown"
  aria-expanded="false"}
  - [Help! My Data Doesn\'t
    Fit!](https://ohdsi.github.io/CommonDataModel/cdmDecisionTree.html)
  - [FAQ](https://ohdsi.github.io/CommonDataModel/faq.html)
  - [SQL
    Scripts](https://ohdsi.github.io/CommonDataModel/sqlScripts.html)
  - [Ask a
    Question](https://ohdsi.github.io/CommonDataModel/contribute.html)

<!-- -->

- [[]{.fa .fa-github}](https://github.com/OHDSI/CommonDataModel)
:::
::::::
:::::::

::: {#header}
# ![](OMOP%20Common%20Data%20Model_files/ohdsi40x40.png) OMOP Common Data Model {#omop-common-data-model .title .toc-ignore}
:::

The Observational Medical Outcomes Partnership (OMOP) Common Data Model
(CDM) is an open community data standard, designed to standardize the
structure and content of observational data and to enable efficient
analyses that can produce reliable evidence.

This website is meant to serve as a resource describing the
specification of the available versions of the Common Data Model. This
includes the structure of the model itself and the agreed upon
conventions for each table and field as decided by the OHDSI Community.
A central component of the OMOP CDM is the OHDSI standardized
vocabularies. The OHDSI vocabularies allow organization and
standardization of medical terms to be used across the various clinical
domains of the OMOP common data model and enable standardized analytics
that leverage the knowledge base when constructing exposure and outcome
phenotypes and other features within characterization, population-level
effect estimation, and patient-level prediction studies. The vocabulary
tables are part of the model and, as such, are detailed here. To
download the vocabulary itself, please visit
[https://athena.ohdsi.org](https://athena.ohdsi.org/). For more
information about the OHDSI suite of tools designed to implement best
practices in characterization, population-level effect estimation and
patient-level prediction, please visit <https://ohdsi.github.io/Hades/>.

If not otherwise specified, all OHDSI content is subject to the
[Creative Commons CC BY-SA
4.0](https://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1)
license.

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: {#the-cdm-working-group .section .level2}
## The CDM Working Group

The CDM is managed by the OHDSI CDM Working Group. If you would like to
join our group please fill out [this
form](https://forms.office.com/Pages/ResponsePage.aspx?id=lAAPoyCRq0q6TOVQkCOy1ZyG6Ud_r2tKuS0HcGnqiQZUOVJFUzBFWE1aSVlLN0ozR01MUVQ4T0RGNyQlQCN0PWcu)
and check "Common Data Model" to be added to our Microsoft Teams
environment. This working group endeavors to maintain the OMOP CDM as a
living model by soliciting and responding to requests from the community
based on use cases and research purposes. For more information on the
CDM refresh process please see the description
[here](http://ohdsi.github.io/CommonDataModel/cdmRefreshProcess.html).
You will find information on our meetings and links to join at the end
of this page.

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: {#calendar .section .level3}
### Calendar

This is the calendar of events for the CDM Working Group, including
upcoming topics and links to meetings. If you would like to present to
the group regarding a new use case for the OMOP CDM or if you would like
the group's assistance with a problem you are having, please fill out
our sign-up form.

[![Sign
Up](OMOP%20Common%20Data%20Model_files/sign-up.png){style="width:15.0%"}](https://www.signupgenius.com/go/10C0948AEAD28A4F9CF8-workgroup)

**Note** If you do you have access to the OHDSI Teams Tenet, either
contact Clair Blacketer at <mblacke@its.jnj.com> or fill out [this
form](https://forms.office.com/Pages/ResponsePage.aspx?id=lAAPoyCRq0q6TOVQkCOy1ZyG6Ud_r2tKuS0HcGnqiQZUOVJFUzBFWE1aSVlLN0ozR01MUVQ4T0RGNyQlQCN0PWcu)
and check "Common Data Model"

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: {.toastui-calendar .calendar .html-widget .html-fill-item .html-widget-static-bound style="width:100%;height:600px;"}
::: {#htmlwidget-f630c4ed99f03a54cd21_menu}
Today

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNTYgMjU2IiBjbGFzcz0icGhvc3Bob3Itc3ZnIiBoZWlnaHQ9IjEuMzNlbSIgZmlsbD0iY3VycmVudENvbG9yIiBzdHlsZT0idmVydGljYWwtYWxpZ246LTAuMjVlbTsiPgogIDxwYXRoIGQ9Ik0xNjQuMjQsMjAzLjc2YTYsNiwwLDEsMS04LjQ4LDguNDhsLTgwLTgwYTYsNiwwLDAsMSwwLTguNDhsODAtODBhNiw2LDAsMCwxLDguNDgsOC40OEw4OC40OSwxMjhaIiAvPgogIDx0aXRsZT5jYXJldC1sZWZ0LWxpZ2h0PC90aXRsZT4KPC9zdmc+){.phosphor-svg}

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNTYgMjU2IiBjbGFzcz0icGhvc3Bob3Itc3ZnIiBoZWlnaHQ9IjEuMzNlbSIgZmlsbD0iY3VycmVudENvbG9yIiBzdHlsZT0idmVydGljYWwtYWxpZ246LTAuMjVlbTsiPgogIDxwYXRoIGQ9Ik0xODAuMjQsMTMyLjI0bC04MCw4MGE2LDYsMCwwLDEtOC40OC04LjQ4TDE2Ny41MSwxMjgsOTEuNzYsNTIuMjRhNiw2LDAsMCwxLDguNDgtOC40OGw4MCw4MEE2LDYsMCwwLDEsMTgwLjI0LDEzMi4yNFoiIC8+CiAgPHRpdGxlPmNhcmV0LXJpZ2h0LWxpZ2h0PC90aXRsZT4KPC9zdmc+){.phosphor-svg}

[2025-11-01 \~ 2025-11-30]{#htmlwidget-f630c4ed99f03a54cd21_renderRange
.render-range}
:::

\

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: {#htmlwidget-f630c4ed99f03a54cd21 .calendar .html-widget .html-widget-static-bound style="width:100%;height:600px;" width="100%" height="600px"}
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: {.toastui-calendar-layout .toastui-calendar-month style="height: 100%; background-color: white;"}
:::::::::::::::::: {.toastui-calendar-day-names .toastui-calendar-month testid="grid-header-month" style="background-color: inherit;"}
::::::::::::::::: {.toastui-calendar-day-name-container style="margin-left: 0px;"}
:::: {.toastui-calendar-day-name-item .toastui-calendar-month style="width: 16.6667%; left: 0%; border-left: medium;"}
[]{style="color: rgb(51, 51, 51);" testid="dayName-month-mon"}

::: toastui-calendar-template-monthDayName
Mon
:::
::::

:::: {.toastui-calendar-day-name-item .toastui-calendar-month style="width: 16.6667%; left: 16.6667%; border-left: medium;"}
[]{style="color: rgb(51, 51, 51);" testid="dayName-month-tue"}

::: toastui-calendar-template-monthDayName
Tue
:::
::::

:::: {.toastui-calendar-day-name-item .toastui-calendar-month style="width: 16.6667%; left: 33.3333%; border-left: medium;"}
[]{style="color: rgb(51, 51, 51);" testid="dayName-month-wed"}

::: toastui-calendar-template-monthDayName
Wed
:::
::::

:::: {.toastui-calendar-day-name-item .toastui-calendar-month style="width: 16.6667%; left: 50%; border-left: medium;"}
[]{style="color: rgb(51, 51, 51);" testid="dayName-month-thu"}

::: toastui-calendar-template-monthDayName
Thu
:::
::::

:::: {.toastui-calendar-day-name-item .toastui-calendar-month style="width: 16.6667%; left: 66.6667%; border-left: medium;"}
[]{style="color: rgb(51, 51, 51);" testid="dayName-month-fri"}

::: toastui-calendar-template-monthDayName
Fri
:::
::::

:::: {.toastui-calendar-day-name-item .toastui-calendar-month style="width: 8.33333%; left: 83.3333%; border-left: medium;"}
[]{.toastui-calendar-holiday-sat style="color: rgb(51, 51, 51);"
testid="dayName-month-sat"}

::: toastui-calendar-template-monthDayName
Sat
:::
::::

:::: {.toastui-calendar-day-name-item .toastui-calendar-month style="width: 8.33333%; left: 91.6667%; border-left: medium;"}
[]{.toastui-calendar-holiday-sun style="color: rgb(255, 64, 64);"
testid="dayName-month-sun"}

::: toastui-calendar-template-monthDayName
Sun
:::
::::
:::::::::::::::::
::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: toastui-calendar-month-daygrid
::::::::::::::::::::: {.toastui-calendar-month-week-item style="height: 16.6667%;"}
:::::::::::::::::::: toastui-calendar-weekday
::::::::::::::::: {.toastui-calendar-weekday-grid style="border-top: 1px solid rgb(229, 229, 229);"}
:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 0%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[27]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgba(51, 51, 51, 0.4);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 16.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[28]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgba(51, 51, 51, 0.4);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 33.3333%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[29]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgba(51, 51, 51, 0.4);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 50%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[30]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgba(51, 51, 51, 0.4);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 66.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[31]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgba(51, 51, 51, 0.4);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 8.33333%; left: 83.3333%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[1]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 8.33333%; left: 91.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[2]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(255, 64, 64);"}
:::
::::
:::::::::::::::::

::: toastui-calendar-weekday-events
:::

::: toastui-calendar-accumulated-grid-selection
:::
::::::::::::::::::::
:::::::::::::::::::::

::::::::::::::::::::: {.toastui-calendar-month-week-item style="height: 16.6667%;"}
:::::::::::::::::::: toastui-calendar-weekday
::::::::::::::::: {.toastui-calendar-weekday-grid style="border-top: 1px solid rgb(229, 229, 229);"}
:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 0%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[3]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 16.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[4]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 33.3333%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[5]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 50%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[6]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 66.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[7]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 8.33333%; left: 83.3333%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[8]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 8.33333%; left: 91.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[9]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(255, 64, 64);"}
:::
::::
:::::::::::::::::

::: toastui-calendar-weekday-events
:::

::: toastui-calendar-accumulated-grid-selection
:::
::::::::::::::::::::
:::::::::::::::::::::

::::::::::::::::::::: {.toastui-calendar-month-week-item style="height: 16.6667%;"}
:::::::::::::::::::: toastui-calendar-weekday
::::::::::::::::: {.toastui-calendar-weekday-grid style="border-top: 1px solid rgb(229, 229, 229);"}
:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 0%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[10]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 16.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[11]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 33.3333%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[12]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 50%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[13]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 66.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[14]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 8.33333%; left: 83.3333%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[15]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 8.33333%; left: 91.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[16]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(255, 64, 64);"}
:::
::::
:::::::::::::::::

::: toastui-calendar-weekday-events
:::

::: toastui-calendar-accumulated-grid-selection
:::
::::::::::::::::::::
:::::::::::::::::::::

::::::::::::::::::::: {.toastui-calendar-month-week-item style="height: 16.6667%;"}
:::::::::::::::::::: toastui-calendar-weekday
::::::::::::::::: {.toastui-calendar-weekday-grid style="border-top: 1px solid rgb(229, 229, 229);"}
:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 0%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[17]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 16.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[18]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 33.3333%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[19]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 50%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[20]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 66.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[21]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 8.33333%; left: 83.3333%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[22]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 8.33333%; left: 91.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[23]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(255, 64, 64);"}
:::
::::
:::::::::::::::::

::: toastui-calendar-weekday-events
:::

::: toastui-calendar-accumulated-grid-selection
:::
::::::::::::::::::::
:::::::::::::::::::::

::::::::::::::::::::: {.toastui-calendar-month-week-item style="height: 16.6667%;"}
:::::::::::::::::::: toastui-calendar-weekday
::::::::::::::::: {.toastui-calendar-weekday-grid style="border-top: 1px solid rgb(229, 229, 229);"}
:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 0%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[24]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 16.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[25]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 33.3333%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[26]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 50%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[27]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 66.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[28]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 8.33333%; left: 83.3333%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[29]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(51, 51, 51);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 8.33333%; left: 91.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[30]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(255, 64, 64);"}
:::
::::
:::::::::::::::::

::: toastui-calendar-weekday-events
:::

::: toastui-calendar-accumulated-grid-selection
:::
::::::::::::::::::::
:::::::::::::::::::::

::::::::::::::::::::: {.toastui-calendar-month-week-item style="height: 16.6667%;"}
:::::::::::::::::::: toastui-calendar-weekday
::::::::::::::::: {.toastui-calendar-weekday-grid style="border-top: 1px solid rgb(229, 229, 229);"}
:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 0%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[1]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgba(51, 51, 51, 0.4);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 16.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[2]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgba(51, 51, 51, 0.4);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 33.3333%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[3]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgba(51, 51, 51, 0.4);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 50%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[4]{.toastui-calendar-weekday-grid-date
.toastui-calendar-weekday-grid-date-decorator
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgb(255, 255, 255);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 16.6667%; left: 66.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[5]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgba(51, 51, 51, 0.4);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 8.33333%; left: 83.3333%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[6]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgba(51, 51, 51, 0.4);"}
:::
::::

:::: {.toastui-calendar-daygrid-cell style="width: 8.33333%; left: 91.6667%; background-color: inherit;"}
::: {.toastui-calendar-grid-cell-header style="height: 31px;"}
[[7]{.toastui-calendar-weekday-grid-date
.toastui-calendar-template-monthGridHeader}]{.toastui-calendar-grid-cell-date
style="color: rgba(255, 64, 64, 0.4);"}
:::
::::
:::::::::::::::::

::: toastui-calendar-weekday-events
:::

::: toastui-calendar-accumulated-grid-selection
:::
::::::::::::::::::::
:::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: {.toastui-calendar-popup-overlay style="display: none;"}
:::

:::::: toastui-calendar-floating-layer
::: toastui-calendar-see-more-popup-slot
:::

::: toastui-calendar-event-form-popup-slot
:::

::: toastui-calendar-event-detail-popup-slot
:::
::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::::: {#current-cdm-version .section .level2}
## Current CDM Version

The current CDM version is [CDM
v5.4](http://ohdsi.github.io/CommonDataModel/cdm54.html), depicted
below. This CDM version was developed over the course of a year by
considering requests that were sent via our [issues
page](https://github.com/OHDSI/CommonDataModel/issues). The list of
proposed changes was then shared with the community in multiple ways:
through discussions at the weekly OHDSI Community calls, discussions
with the OHDSI Steering Committee, and discussions with all potentially
affected workgroups. The [final
changes](http://ohdsi.github.io/CommonDataModel/cdm54Changes.html) were
then delivered to the Community through a new R package designed to
dynamically generate the DDLs and documentation for all supported SQL
dialects. Looking for an entity-relationshop diagram? Click
[here](http://ohdsi.github.io/CommonDataModel/cdm54erd.html)!

- [Link to DDLs for CDM
  v5.4](https://github.com/OHDSI/CommonDataModel/tree/v5.4.0/inst/ddl/5.4)
- [Link to ReadMe for instructions on how to use the R
  package](https://github.com/OHDSI/CommonDataModel/tree/master#readme)

![](OMOP%20Common%20Data%20Model_files/cdm54.png)\

::: {#current-support-for-cdm-v5.4 .section .level3}
### Current Support for CDM v5.4

The table below details which OHDSI tools support CDM v5.4. There are
two levels of support: legacy support means that the tool supports all
tables and fields that were present in CDM v5.3 and feature support
indicates that the tool supports any new tables and fields in CDM v5.4
that were not present in CDM v5.3. A green check ✔️ indicates that the
support level for the listed tool is in place, has been tested, and
released. A warning sign ❗ indicates that the support level for the
listed tool has been initiated but has not yet been tested and
released.\

  ------------------------------------------------------------------------------------------------------------
  **Tool**              **Description**                                    **Legacy          **Feature
                                                                           Support**         Support**
  --------------------- -------------------------------------------------- ----------------- -----------------
  **CDM R package**     This package can be downloaded from                ✔️                ✔️
                        <https://github.com/OHDSI/CommonDataModel/>. It                      
                        functions to dynamically create the OMOP CDM                         
                        documentation and DDL scripts to instantiate the                     
                        CDM tables.                                                          

  **Data Quality        This package can be downloaded from                ✔️                ❗
  Dashboard**           <https://github.com/OHDSI/DataQualityDashboard>.                     
                        It runs a set of \> 3500 data quality checks                         
                        against an OMOP CDM instance and is required to be                   
                        run on all databases prior to participating in an                    
                        OHDSI network research study.                                        

  **Achilles**          This package can be downloaded from                ✔️                ❗
                        <https://github.com/OHDSI/Achilles>, performing a                    
                        set of broad database characterizations against an                   
                        OMOP CDM instance.                                                   

  **ARES**              This package can be downloaded from                ✔️                ❗
                        <https://github.com/OHDSI/Ares> and is designed to                   
                        display the results from both the ACHILLES and                       
                        DataQualityDashboard packages to support data                        
                        quality and characterization research.                               

  **ATLAS**             ATLAS is an open source software tool for          ✔️                ❗
                        researchers to conduct scientific analyses on                        
                        standardized observational data.                                     
                        [Demo](http://atlas-demo.ohdsi.org/)                                 

  **Rabbit-In-A-Hat**   This package can be downloaded from                ✔️                ✔️
                        <https://github.com/OHDSI/WhiteRabbit> and is an                     
                        application for interactive design of an ETL to                      
                        the OMOP Common Data Model with the help of the                      
                        the scan report generated by White Rabbit.                           

  **Feature             This package can be downloaded from                ✔️                ✔️\*
  Extraction**          <https://github.com/OHDSI/FeatureExtraction>. It                     
                        is designed to generate features (covariates) for                    
                        a cohort generated using the OMOP CDM.                               

  **Cohort              This package can be downloaded from                ✔️                ❗
  Diagnostics**         <https://github.com/OHDSI/CohortDiagnostics> and                     
                        is used to critically evaluate cohort phenotypes.                    
  ------------------------------------------------------------------------------------------------------------

\
\* The **Feature Extraction** package supports all relevant new features
in CDM v5.4. For example, it was decided that, from a methodological
perspective, the EPISODE and EPISODE_EVENT tables should not be included
to define cohort covariates because the events that make up episodes are
already pulled in as potential covariates.

\
:::

::: {#cdm-wg-important-links .section .level3}
### CDM WG Important Links

- [Google Drive
  Location](https://drive.google.com/open?id=1DaNKe6ivIAZPJeI31VJ-pzNB9wS9hDqu)
- [Running
  Agenda](https://docs.google.com/document/d/1WgKePjrI_cGdqn2XQCe1JdGaTzdMqU4p5ihkMt8fcAc/edit?usp=sharing)
- [CDM Github](https://github.com/OHDSI/CommonDataModel)
- [Process for adopting CDM and Vocabulary
  changes](http://ohdsi.github.io/CommonDataModel/cdmRefreshProcess.html)
:::
:::::
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: {#custom-bm-menu-trigger}
📟
:::

:::::: {#custom-bm-menu-container}
[✨
SUMMARIZE[(selectAll)]{.custom-bm-select-all}](#){.custom-bm-menu-item}[💾
SAVE_MARKDOWN](#){.custom-bm-menu-item}[♓ Get it at
Harvard!](#){.custom-bm-menu-item}[🎞️
mp4\[0\]](#){.custom-bm-menu-item}[⤵️
sortScholar](#){.custom-bm-menu-item}[💬 Talk to
ChatGPT[(selectAll)]{.custom-bm-select-all}](#){.custom-bm-menu-item}[🍊
ask
Claude[(selectAll)]{.custom-bm-select-all}](#){.custom-bm-menu-item}[🔷
Copy Gemini
Prompt[(selectAll)]{.custom-bm-select-all}](#){.custom-bm-menu-item}[🤖
Generate & Run Code](#){.custom-bm-menu-item}

::: custom-bm-separator
:::

:::: {.custom-bm-menu-item .custom-bm-has-submenu}
[▾]{.submenu-arrow} 🛒 multi-page, etc.

::: custom-bm-submenu
[🛒 Add to Basket](#){.custom-bm-menu-item}[📋 View
Basket](#){.custom-bm-menu-item}[🗑️ Clear
Basket](#){.custom-bm-menu-item}[📚 Summarize
Basket](#){.custom-bm-menu-item}[🤖 ChatGPT
Basket](#){.custom-bm-menu-item}[🧠 Claude
Basket](#){.custom-bm-menu-item}[💎 Gemini
Basket](#){.custom-bm-menu-item}[🚫 Hide Menu
App](#){.custom-bm-menu-item}
:::
::::
::::::
