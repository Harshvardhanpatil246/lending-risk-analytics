# Problem Statement: Lending Risk & Portfolio Analytics

## 1. Background

A lending company gives personal loans to people online.
Some borrowers stop paying, and the company loses that money.
Right now, these losses are too high.
The company wants to lose less money, but without losing too much business.

## 2. Stakeholders

| Who | What they want |
|---|---|
| **Head of Risk** (main stakeholder) | Fewer bad loans and lower losses |
| Sales / Growth team | More approved loans and more business |
| Finance team | Higher profit (interest earned minus money lost) |

These goals pull in different directions.
Rejecting more people cuts losses, but it also cuts business.
Our job is to show this trade-off clearly, with numbers.

## 3. The decision

> **Which loans should we stop approving?**
> For each option: how many loans do we lose, how much loss do we avoid, and what happens to profit?

## 4. Key questions

1. **Who goes bad most?** Which borrower groups have the highest bad rate (by grade, purpose, term, income, DTI, FICO score, state)?
2. **Is the price right?** Is the interest rate high enough to cover the risk of each group?
3. **Is it getting worse?** Did newer loans go bad more often than older loans, when we compare them at the same age (vintage analysis)?
4. **Can we predict it?** Using only what we know on the day of approval, can we estimate how likely a borrower is to go bad?
5. **What does each choice cost?** If we stop approving a group, how many loans do we lose, how much loss do we avoid, and what happens to profit?

## 5. Scope

**In scope**
- Approved loans from Lending Club, 2007 to 2020 Q3
- Rejected applications from Lending Club, 2007 to 2018
- USA only
- To predict risk, we use only information known on the day of approval

**Out of scope** (we will not do this)
- Live (real-time) scoring of new applications
- How to collect money from late borrowers (collections)
- Economy data, such as unemployment
- Setting new interest rates (we only check if the current rates are high enough)

## 6. Success metrics

The Head of Risk will compare the options using these numbers:

| Metric | Simple meaning |
|---|---|
| Bad rate | % of finished loans that went bad |
| Loss avoided ($) | Money we would not have lost, if we had rejected these loans |
| Loans lost (count and %) | Business we give up by rejecting more people |
| Interest income lost ($) | Interest we would no longer earn from those loans |
| Net effect on profit ($) | Loss avoided minus interest income lost |
| Approval rate | % of applications approved, before and after the change |

The exact formulas are written in `docs/metric_definitions.md`.

**The project is successful if:**
- The Head of Risk gets **3 clear options**, each with the numbers above.
- The trade-off for each option is easy to see.
- Every number can be rebuilt from the data pipeline.

## 7. Data limits and assumptions

- **Old, US-only data:** approved loans end in 2020 Q3; rejected applications end in 2018.
- **Selection bias:** we only see what happened to approved loans. We never know if rejected people would have paid.
- **Unfinished loans:** loans that are still running ("Current") are not finished. We do not count them as good loans.
- **Rules changed over time:** some old loans are marked "Does not meet the credit policy". We will decide how to treat them.
- **Simple profit:** profit = interest earned minus money lost. We ignore fees and the company's own costs.

## 8. Deliverables

| What | Where |
|---|---|
| Data pipeline: download, load, clean, test | `ingestion/`, `dbt/`, `orchestration/` |
| Metric definitions | `docs/metric_definitions.md` |
| Analysis: data exploration, vintage, risk model, policy options | `notebooks/` |
| Power BI dashboard (3 pages) | `dashboard/` |
| One-page decision memo for the Head of Risk | `docs/decision_memo.md` |
