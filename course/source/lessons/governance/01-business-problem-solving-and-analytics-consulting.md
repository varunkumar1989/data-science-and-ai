---
num: 1
title: Business Problem-Solving: KPIs, Process Mapping, Discovery and Hypotheses
live: "Gap-fill lesson"
updated: "2026"
level: Intermediate
duration: 120 min
summary: Turn a vague business complaint into a measurable problem. Define KPIs and the drivers beneath them, map a process to find its bottleneck, run stakeholder discovery with Five Whys and a fishbone diagram, and write testable hypotheses and recommendations with an owner and a measure.
datasets: [superstore_sales.csv]
outcomes:
  - Link a business goal to a KPI and its driver metrics
  - Map a process step by step and find the bottleneck and the cost of delay
  - Run discovery with interviews, Five Whys and a fishbone analysis
  - Write a hypothesis, the data it needs and a recommendation with a measure
---

## From complaint to problem

Business requests arrive as complaints: "sales are down", "the reports are slow", "customers are unhappy". Analytics consulting starts by turning a complaint into a **problem statement**: who is affected, what happens, how much it costs, and how often. A problem statement is measurable, so it can be tested and solved.

:::case Late deliveries
A distribution manager says "deliveries are often late". Before any analysis, the consultant asks: late by how much, for which customers, since when, compared with what target? The answer becomes a problem statement: "12% of orders in the north region arrive more than one day late, costing about 300 repeat orders a month, mostly for orders placed after 3 p.m." Now there is something to measure.
:::

## KPIs and driver metrics

A **KPI** (key performance indicator) is a measured result tied to a goal. A **driver metric** is an input that moves the KPI. Start from the goal, choose the KPI that measures progress towards it, and then find the drivers the team can actually change.

| Goal | KPI | Driver metrics |
|---|---|---|
| Customers get orders on time | On-time delivery rate | Stock availability at dispatch, pick time, carrier lead time |
| Grow revenue sustainably | Gross margin | Discount depth, product mix, return rate |
| Faster loan decisions | Time to approval (days) | Documents received on day 1, underwriter queue length |

Two rules keep KPIs honest: one owner per KPI, and a definition written down (what counts, what is excluded, which source). A KPI without a definition is a number that people argue about.

## Business models in one sentence

A business model explains how money is made: who pays, for what, and at what cost to serve. Write it in one sentence before you analyse anything: "We earn a margin on each product sold through three channels, and our cost of serving a customer rises when returns are high." The sentence tells you which KPIs matter.

## Process mapping

**Process mapping** shows each step of a workflow, who owns it, how long it takes and where work waits. Draw it as a sequence of boxes with times and handoffs, then mark the bottleneck: the step where work queues up, and the cost of delay there.

```python run
import pandas as pd

# A loan approval process, step by step, with the average days each step takes
steps = pd.DataFrame({
    "step": ["application received", "document collection", "credit check",
             "underwriter review", "decision letter sent"],
    "owner": ["sales", "customer", "risk system", "underwriter", "operations"],
    "days": [0.5, 5.0, 0.5, 2.0, 1.0],
})
steps["cumulative_days"] = steps["days"].cumsum()
steps["share_of_total"] = (steps["days"] / steps["days"].sum()).round(2)
print(steps.to_string(index=False))
print("bottleneck:", steps.loc[steps["days"].idxmax(), "step"])
```

The longest step is the bottleneck: here, document collection takes most of the nine days. Improving the underwriter review, however fast, cannot shorten the total by more than the time it occupies.

## Discovery: interviews, Five Whys and fishbone

**Discovery** gathers the facts before anyone proposes a solution. Three tools do most of the work:

1. **Stakeholder interviews.** Speak to five to eight people across roles: the person who raised the complaint, the people who do the work, the people who receive the output, and someone who sees the data. Ask about the last time it went wrong, not about opinions.
2. **Five Whys.** Ask "why" repeatedly until the answer is a process or system you can change. Usually five levels are enough.
3. **Fishbone (Ishikawa) diagram.** Group the causes under categories: people, process, tools, data, and environment. It makes sure no category is ignored.

| Why | Answer |
|---|---|
| Why are deliveries late? | Stock is out at dispatch. |
| Why is stock out? | The forecast underestimated demand. |
| Why was the forecast wrong? | It used sales data that was a week old. |
| Why is the data a week old? | The sales load runs weekly, not daily. |
| Why weekly? | Nobody has reviewed the schedule since the old system. |

The root cause is the weekly load, which is a schedule you can change. The fishbone diagram shows whether other categories (for example, slow pick times) also contribute.

::::warn Stop at the changeable cause
Five Whys can end in a cause nobody controls ("because people are busy"). Keep asking until you reach a process, a system, a rule or a decision that the team can change.
::::

## Hypotheses and analytical questions

A **hypothesis** is a testable statement that says what you expect to see and what would prove it wrong. Write the business question, then the hypothesis, then the data needed.

| Question | Hypothesis | Data needed | What would prove it wrong |
|---|---|---|---|
| Why do customers miss appointments? | A reminder email reduces misses by 15% | Appointment log, reminder send log | No difference between reminded and control groups |
| Why did margin fall? | Discount depth rose in one region | Orders with discount, by region and month | Discount rate unchanged in that region |

Test the hypothesis with data before you recommend anything. For the reminder example, an A/B split over four weeks is the test: half the customers get the reminder, half do not, and the difference is measured.

## Recommendations with an owner and a measure

A recommendation says what to do, who does it, when, and how you will know it worked. A recommendation without a measure is an opinion.

**Template:** "We recommend [action] because [evidence]. [Owner] will [do it] by [date]. We will know it worked when [measure] moves from [baseline] to [target] within [timeframe]."

:::interview How do you start an analytics consulting engagement?
Clarify the decision the work must support, interview five to eight people across roles, write the problem statement with who, what, cost and frequency, and map the process to find where time or money is lost. Then state the hypothesis you will test first, and agree the measure of success with the sponsor before any analysis.
:::

::::key What to remember
- Turn complaints into measurable problem statements.
- Link goals to KPIs, and KPIs to the drivers the team can change.
- Map the process to find the bottleneck, which decides where effort pays.
- Run discovery with interviews, Five Whys and a fishbone; stop at a changeable cause.
- Test hypotheses with data, and recommend with an owner and a measure.
::::

:::quiz
Q: What is a driver metric?
- A metric that the CEO chooses
* An input that moves a KPI and that the team can influence
- A list of drivers on a road
- The final result of a goal
> Drivers are the levers beneath the KPI.

Q: In a process map, which step matters most for reducing total time?
- The shortest step
* The bottleneck, where work waits longest
- The first step always
- The last step always
> Speeding up non-bottleneck steps barely changes the total.

Q: Five Whys ends at "because people are busy". What should you do?
- Accept it
* Keep asking until the cause is a process or system the team can change
- Stop and report
- Ignore the answer
> Root causes must be changeable.

Q: Which hypothesis is testable?
- Our customers are unhappy
* A reminder email reduces missed appointments by 15%, measured with a control group
- Everything will improve
- The data is interesting
> A testable hypothesis names an expected, measurable effect.

Q: What makes a recommendation complete?
- A long list of charts
* An action, an owner, a date and a measure with a baseline and target
- A statement of opinion
- A budget only
> Ownership and measurement make recommendations actionable.
:::

:::exercise Diagnose a problem
Choose a real or invented business complaint (for example, "customer complaints have doubled"). Write the problem statement, one KPI with two driver metrics, a five-step process map with the bottleneck marked, a five-whys chain to a changeable cause, and one testable hypothesis with its test design and a recommendation template filled in.
???
Hints: state the baseline and the period in the problem statement. In the process map, put owners and days on each step. In the test design, name the control group and the minimum period before you read the result.
:::
