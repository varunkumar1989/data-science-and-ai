---
num: 2
title: Requirements, User Stories, PRDs, Data Storytelling and Agile Delivery for Analytics
live: "Gap-fill lesson"
updated: "2026"
level: Intermediate
duration: 120 min
summary: Specify analytics work so that it gets built right the first time. Write requirements, user stories and acceptance criteria, draft a product requirements document, communicate findings with data storytelling, and run analytics delivery in short agile cycles with a backlog, sprints and reviews.
datasets: []
outcomes:
  - Write user stories with acceptance criteria that can be tested
  - Separate functional and non-functional requirements
  - Draft a short product requirements document for an analytics product
  - Structure a data story and run agile delivery with a backlog and sprint reviews
---

## Requirements are a contract about meaning

Most failed analytics projects were not technically hard. They built what was asked, and the person asking meant something different. A requirement is a statement of what the solution must do, written so that the builder and the user agree on the meaning. Writing it down is cheaper than rebuilding a dashboard three times.

:::case The dashboard nobody used
A team built a churn dashboard with forty charts. The sponsor wanted to decide, each Monday, which customers to call. The dashboard answered many questions and none of the Monday decision. A short user story, "As the retention lead, I want a Monday list of customers at risk, so that I can call the top 50 before Wednesday", would have shaped a single table and saved six weeks.
:::

## User stories and acceptance criteria

A **user story** describes value from the user's point of view:

> As a **[role]**, I want **[need]**, so that **[benefit]**.

The benefit matters most. It tells the builder which details are essential and which are decoration. An **acceptance criterion** says how to test that the story is done, using the form:

> Given **[context]**, when **[action]**, then **[result]**.

**Example.** As an operations manager, I want a daily list of late orders, so that I can call customers before 10:00.

| Acceptance criterion | Test |
|---|---|
| Given an order is 2 hours or more late, when the list is generated at 07:00, then the order appears on the list | Create a late test order; check the list |
| Given an order was delivered, when the list is generated, then the order does not appear | Check a delivered order is excluded |
| Given there are no late orders, when the list is generated, then the list shows "no late orders today" | Run on a day with zero late orders |

Each criterion is a test. If a criterion cannot be tested, rewrite it until it can.

## Functional and non-functional requirements

**Functional** requirements say what the solution does. **Non-functional** requirements say how well it does it: speed, accuracy, security, availability, cost, and how long data may be kept.

| Type | Example |
|---|---|
| Functional | The list shows order id, customer, days late and the owner |
| Performance | The list is ready by 07:00 for 95% of days |
| Accuracy | Days late matches the logistics system within one hour |
| Security | Only the operations team can see customer contact details |
| Availability | The list is available during working hours, 99% of days |

Non-functional requirements are often forgotten and then cause the most expensive rework. Write them down at the start.

## A short PRD

A **product requirements document (PRD)** gathers the story, the requirements and the success measures for a product, in one or two pages. For an analytics product, a useful PRD has these sections:

1. **Problem and decision.** The problem statement and the decision the product supports.
2. **Users and their stories.** Each user role with its stories and acceptance criteria.
3. **Data.** Sources, grain, freshness and owners.
4. **Requirements.** Functional and non-functional, with priority (must, should, could).
5. **Out of scope.** What is deliberately not included.
6. **Success measures.** The metric and target, and how it will be measured after launch.
7. **Open questions.** What must be answered, by whom and by when.

::::tip The out-of-scope section protects the team
Most scope creep arrives as a "small addition". A written out-of-scope list lets the team say "that is a good idea for the next version" with a reason, rather than negotiating it from scratch each time.
::::

## Data storytelling

A data story turns findings into a decision. The usual structure is short:

1. **The answer first.** One sentence: "Churn rose four points in March, driven by two plans."
2. **The evidence.** One chart per message, labelled so that it can be read without the speaker.
3. **The decision.** What should happen, who owns it, and by when.

| Weak | Stronger |
|---|---|
| "Here are twelve charts about churn." | "Churn rose four points in March. Fix onboarding for the two plans driving it by 15 May." |
| A chart with no title and a rainbow palette | A chart titled with its message, one highlighted series |
| Ending with "any questions?" | Ending with the decision needed and the owner |

The same data can support different stories for different audiences. An executive needs the decision; an analyst needs the method. Prepare the first slide for the decision and keep the method in an appendix.

## Agile delivery for analytics

**Agile** delivers work in short cycles, so that the user sees something useful early and changes direction cheaply. The core parts are:

| Part | What it is | Analytics example |
|---|---|---|
| Backlog | Work ordered by value | "Late order list", "churn drivers", "margin by region" |
| Sprint | A fixed period, usually one or two weeks, with a goal | Sprint goal: first version of the late order list |
| Review | Showing the increment to stakeholders | Demo to the operations manager with real data |
| Retrospective | What to improve in the way the team works | The data delay was found too late; add a freshness check |

**Kanban** is an alternative that shows work moving across columns (to do, in progress, review, done) and limits the number of items in progress. It suits support-style analytics work with unpredictable requests.

Delivery management adds three controls: a scope list that changes only through the backlog, a risk register that names the risks and their owners, and a dependency list that shows which work waits for which data or person.

:::interview How do you keep an analytics project from drifting?
Write the problem statement and the user stories first, with acceptance criteria. Keep the scope in a backlog with an out-of-scope list. Deliver a first version within a sprint and review it with the user on real data. Each change goes through the backlog with its benefit stated, so that the trade-off is visible.
:::

::::key What to remember
- Write user stories with a benefit and acceptance criteria that can be tested.
- Specify non-functional requirements (speed, accuracy, security, availability) early.
- A PRD states the decision, the users, the data, the requirements, the out-of-scope list and the success measures.
- Storytelling: the answer first, one chart per message, and the decision with an owner.
- Deliver in short cycles, review on real data, and change scope through the backlog.
::::

:::quiz
Q: What is the most important part of a user story?
- The number of words
* The benefit, which shows what matters most to the user
- The author's name
- The tool to use
> The benefit guides what is essential.

Q: Which is a valid acceptance criterion?
- The dashboard should look nice
* Given an order is two hours late, when the list runs at 07:00, then the order appears on it
- Users will be happy
- The data should be fast
> A criterion has a context, an action and a testable result.

Q: Why write non-functional requirements at the start?
- They are required by agile
* They are often forgotten and cause the most expensive rework when discovered late
- They replace functional requirements
- They are optional
> Speed, security and accuracy shape the design.

Q: In data storytelling, what should come first?
- The method
- The list of charts
* The answer in one sentence
- The thank-you slide
> The answer first respects the audience's time.

Q: What is the purpose of a sprint review?
- To close the project
* To show the working increment to stakeholders and gather feedback on real data
- To assign blame
- To choose the tool
> Reviews make feedback concrete and early.
:::

:::exercise Write the spec for one dashboard
Write a one-page PRD for a dashboard that a sales manager will use each Monday: the decision, two user stories with three acceptance criteria each, four non-functional requirements, the out-of-scope list, two success measures and two open questions. Then write a three-sentence data story for its first review.
???
Hints: make each acceptance criterion testable against the data. Put at least one security requirement in the non-functional list. The data story must lead with the answer, even if the answer is a question the dashboard will settle.
:::
