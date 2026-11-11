---
num: 6
title: Business Scenario Interviews: Seven Problems and Answer Frameworks
live: "Gap-fill lesson"
updated: "2026"
level: Intermediate
duration: 120 min
summary: Practise seven open-ended business scenarios, from a sales decline and rising churn to a slow dashboard, a failed pipeline, an incorrect AI assistant and a vague stakeholder request. Each has a structured answer framework: clarify, hypothesise, analyse, recommend and measure.
datasets: []
outcomes:
  - Structure an open-ended business answer with a repeatable framework
  - Ask the clarifying questions that show judgement before analysing
  - Propose tests and measures, not only conclusions
  - Recognise when the right answer is "I need to clarify the requirement first"
---

## What a scenario interview tests

Scenario questions have no single right answer. The interviewer is judging how you think: whether you clarify before you analyse, whether your hypotheses are specific enough to test, whether you choose the cheapest test that would change a decision, and whether you can recommend an action and say how you will know it worked.

## The framework

Use the same five steps for every scenario, and say the step names aloud.

1. **Clarify.** What exactly happened, over what period, for which segment, compared with what? Ask two or three questions before answering.
2. **Hypothesise.** List three to five possible causes, ranked by how likely and how cheap they are to check.
3. **Analyse.** For each hypothesis, name the data that would confirm or reject it, and the test or query you would run.
4. **Recommend.** State the most likely cause and the action, with the trade-off.
5. **Measure.** Name the metric that will show the action worked, and the timeframe.

## Scenario 1: sales have declined by 20%

- **Clarify:** Which products, regions and channels? Compared with last month, last year, or the plan? Did prices, stock or the sales team change?
- **Hypotheses:** a data or reporting change; a seasonal effect; lost customers; lower traffic; a stock-out; a price change; a competitor move.
- **Analysis:** split the decline by region, product, channel and customer type; compare new and repeat customers; check whether the drop comes from fewer orders or smaller orders; reconcile the total with the finance ledger.
- **Recommend:** act on the largest confirmed driver only. If the data is wrong, the first action is to fix the data.
- **Measure:** weekly sales in the affected segment against a comparison group.

## Scenario 2: customer churn has increased

- **Clarify:** How is churn defined (cancellation, or no order for 90 days)? Which customer groups? Since when?
- **Hypotheses:** a price increase; a product issue; a support problem; a competitor offer; a cohort acquired through a weak channel.
- **Analysis:** cohort retention by sign-up month and channel; the tenure at which customers leave; support tickets before churn; the share of churners who used a discount.
- **Recommend:** a targeted retention offer for the group most at risk, with a control group to measure it.
- **Measure:** retention of the treated group against the control after 60 to 90 days.

## Scenario 3: a dashboard is slow

- **Clarify:** How slow, for whom, and since when? Which filters? Is it the first load or each interaction?
- **Hypotheses:** too much data in the model; inefficient measures; too many visuals; a slow data source; unlimited filters.
- **Analysis:** check the query and refresh timings; count the rows loaded; find the measures that scan the most data.
- **Recommend:** aggregate the fact table to the level the dashboard needs, simplify the most expensive measures, and reduce the visuals on the first page.
- **Measure:** time to first render, p95, and user feedback.

## Scenario 4: a data pipeline has failed

- **Clarify:** Which job, which step, what error, since when, and what depends on it? Is it the first failure or a repeat?
- **Hypotheses:** a source schema change; a late file; a permission change; a memory limit; a bad record; a changed API.
- **Analysis:** read the logs at the failing step; compare row counts with the previous run; check upstream jobs and the source schema.
- **Recommend:** restore service first (rerun the failed partition if the job is idempotent), then fix the cause and add a test that would have caught it.
- **Measure:** time to detect and time to recover, and whether the same failure recurs.

## Scenario 5: an AI assistant gives incorrect answers

- **Clarify:** Which questions, how often, and how wrong? Did the assistant have the right documents? Was the answer checked by a person?
- **Hypotheses:** retrieval missed the right document; the document is out of date; the prompt allows guessing; the model is wrong on a specific topic; a tool returned bad data.
- **Analysis:** build a test set of the failing questions; check whether the right passage was retrieved; read the answers against the sources; check tool outputs.
- **Recommend:** fix the cause that the test points to (retrieval, content, prompt or tool), and add the cases to the regression suite.
- **Measure:** accuracy on the test set and the rate of wrong answers reported by users.

## Scenario 6: an enterprise customer wants to automate a manual workflow

- **Clarify:** What is the workflow today, how long does it take, how often, what goes wrong, and who approves each step?
- **Hypotheses:** the workflow is fixed (a workflow tool suffices); it needs judgement at some steps (an agent with approval); the data is not ready.
- **Design:** map the steps; mark each as deterministic, model-driven or needing a person; choose the simplest tool; define the approval points, the data access and the logs.
- **Recommend:** a pilot on one part of the workflow with a clear success measure and a stop rule.
- **Measure:** time per case, error rate, the share handled without a person, and cost per case.

## Scenario 7: a stakeholder asks for a dashboard but cannot define the requirements

- **Clarify:** What decision will this dashboard support? Who will use it, and how often? What would they do differently if it showed X?
- **Hypotheses:** the stakeholder knows the problem but not the measures; they need an example before they can specify.
- **Approach:** run a short discovery: interview two users, sketch three layouts on paper, and agree the first three questions the dashboard must answer.
- **Recommend:** build a first version with the three agreed questions, show it, and collect changes.
- **Measure:** whether the stakeholder uses it in a real meeting within a month.

:::interview The strongest answer to a vague request
Say that you would not build anything yet. Explain the decision the work must support, propose a 30-minute discovery session, and describe the smallest version you would show within a week. Interviewers reward candidates who protect the team from building the wrong thing.
:::

::::key What to remember
- Clarify before analysing; two good questions show judgement.
- Rank hypotheses by likelihood and by how cheap they are to test.
- Recommend one action with its trade-off, and name the measure that proves it worked.
- For a vague request, the first deliverable is a decision and a shared definition.
::::

:::quiz
Q: What is the first step in answering a scenario question?
- Recommend an action
- Build a chart
* Clarify what exactly happened, over what period, and compared with what
- Name the tool to use
> Analysis without a clear question wastes effort.

Q: Which hypothesis should you test first in a sales decline?
- The one you like best
* The likely cause that is cheapest to check, such as a data change
- The one that needs the most budget
- The competitor's product launch
> Ranking by likelihood and cost focuses effort.

Q: The dashboard is slow. Which fix comes first?
- Buy a faster computer
* Check where time is spent, then aggregate or simplify the costliest parts
- Add more visuals
- Remove all measures
> Measure before optimising.

Q: A pipeline fails. What is the right order of actions?
- Fix the code and then tell someone
* Restore service where safe, then fix the cause and add a test
- Delete the logs
- Wait for the next scheduled run
> Recovery first, then prevention.

Q: A stakeholder cannot define a requirement. What should you do?
- Build the most complete dashboard possible
- Refuse the work
* Run a short discovery to agree the decision and the first questions
- Ask for a bigger budget
> The first deliverable is a shared definition of the problem.
:::

:::exercise Answer two scenarios
Choose two of the seven scenarios and answer each in four minutes using the five-step framework, out loud or in writing. For each, state the first two clarifying questions, your top three hypotheses, the test you would run first, and the measure you would report.
???
Hints: keep the answer within the five headings. Make the first test specific enough to run this week. If you do not know a number, say how you would obtain it.
:::
