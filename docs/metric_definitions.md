# Metric Definitions

**One number, one meaning.**
Every number in this project (notebooks, dashboard, memo) uses the rules in this file.

- All examples use **made-up numbers**, only to explain the idea.
- All money is in US dollars ($).

---

## 0. Words used in this file

| Word | Simple meaning |
|---|---|
| Loan amount | The money we lent |
| Principal paid back | The part of the loan money the borrower gave back (not counting interest) |
| Interest | The extra money the borrower pays us for borrowing |
| Recoveries | Money we still collect after a loan has gone bad |
| Collection fee | What we pay an agency to collect that money |
| Finished loan | A loan that is good or bad (see section 1) |

---

## 1. Loan outcome rule: good, bad or not finished?

Every loan goes into **one** of 3 groups:

| Loan status | Group | Why |
|---|---|---|
| Fully Paid | ✅ **Good** | All money paid back |
| Charged Off | ❌ **Bad** | We wrote it off as lost money |
| Default (121+ days late) | ❌ **Bad** | Almost always becomes Charged Off |
| Late (31–120 days) | ⏳ **Not finished** | Still running. Some borrowers catch up |
| Late (16–30 days) | ⏳ **Not finished** | Still running |
| In Grace Period | ⏳ **Not finished** | Still running |
| Current | ⏳ **Not finished** | Still running, paying on time |
| Does not meet the credit policy. Status: X | Same group as X | Old loans from older rules. We mark them with a flag (`is_old_credit_policy`) so we can remove them if needed |

**Important:** not-finished loans are **left out** of the bad rate, loss rate and LGD.
**Why?** They may still go bad. Counting them as good makes the bad rate look too low.

---

## 2. Loan metrics

### 2.1 Bad rate
- **In simple words:** out of the finished loans, how many went bad?
- **Formula:** bad loans ÷ (good loans + bad loans)
- **Example:** 80 good, 20 bad, 50 not finished
  → 20 ÷ (80 + 20) = **20%**
  (The 50 not-finished loans are **not** counted.)

### 2.2 EAD (Exposure at Default)
- **In simple words:** how much money was still owed when the loan went bad?
- **Formula:** loan amount − principal paid back
- **Example:** we lent $10,000, the borrower paid back $4,000
  → 10,000 − 4,000 = **$6,000 still owed**

### 2.3 Net loss
- **In simple words:** how much money did we really lose on a bad loan?
- **Formula:** EAD − (recoveries − collection fee)
- **Example:** $6,000 still owed. We collected $1,000 later, but paid a $100 fee to collect it.
  → we really got back 1,000 − 100 = $900
  → 6,000 − 900 = **$5,100 lost**
- Good loans have a net loss of **$0**.

### 2.4 LGD (Loss Given Default)
- **In simple words:** when a loan goes bad, what % of the money still owed do we never get back?
- **Formula:** net loss ÷ EAD
- **Example:** lost $5,100 out of $6,000 owed
  → 5,100 ÷ 6,000 = **85%**

### 2.5 Loss rate
- **In simple words:** out of all the money we lent, what % did we lose?
- **Formula:** total net loss ÷ total loan amount (finished loans only)
- **Example:** 100 finished loans of $10,000 each = $1,000,000 lent.
  20 of them went bad and each lost $5,100 → 20 × 5,100 = $102,000 lost
  → 102,000 ÷ 1,000,000 = **10.2%**

### 2.6 Approval rate
- **In simple words:** out of everyone who applied, what % did we approve?
- **Formula:** approved applications ÷ (approved + rejected applications)
- **Example:** 150 approved, 850 rejected
  → 150 ÷ 1,000 = **15%**
- **Only for 2007–2018.** The rejected data ends in 2018. After 2018 we only see approved loans, so the rate would wrongly look like 100%.

### 2.7 Expected loss (EL)
- **In simple words:** on average, how much do we expect to lose on a loan?
- **Formula:** PD × LGD × EAD
  - PD = the chance the loan goes bad. It comes from the risk model (Phase 7). For a whole group, we can use the group's bad rate.
- **Example:** 20% chance of going bad, we lose 85% of what is owed, $6,000 owed
  → 0.20 × 0.85 × 6,000 = **$1,020**

### 2.8 Interest income
- **In simple words:** how much interest did the borrower pay us?
- **Formula:** total interest paid by the borrower
- **Example:** $10,000 loan, 12% per year, 36 months, all paid → about **$1,957**
- Bad loans also pay **some** interest before they stop paying.

### 2.9 Risk-adjusted return
- **In simple words:** after losses, how much did we really earn?
- **Formula:** (interest income − net loss) ÷ loan amount
- **Example:** we lent $1,000,000, earned $150,000 interest, lost $102,000
  → (150,000 − 102,000) ÷ 1,000,000 = **4.8%**

---

## 3. Policy metrics: "What if we stop approving group X?"

These use **finished loans only**, so we know the result of every loan.

### 3.1 Loans lost
- **In simple words:** how many loans would the new rule reject?
- **Formula:** number of loans the new rule rejects (also as % of all loans)
- **Example:** the rule rejects 100 out of 1,000 loans → **100 loans (10%)**

### 3.2 Loss avoided
- **In simple words:** how much loss would we NOT have, if we had rejected those loans?
- **Formula:** total net loss of the loans the new rule rejects
- **Example:** those 100 loans lost **$50,000** in total

### 3.3 Interest income lost
- **In simple words:** how much interest would we NOT earn, if we had rejected those loans?
- **Formula:** total interest income from the loans the new rule rejects (good and bad)
- **Example:** those 100 loans paid us **$30,000** in interest

### 3.4 Net effect on profit
- **In simple words:** is the new rule worth it?
- **Formula:** loss avoided − interest income lost
- **Example:** 50,000 − 30,000 = **+$20,000** → the rule **makes** money ✅
- If the answer is **below $0**, the rule **costs** money ❌

---

## 4. Notes

- Every metric can be split by group: grade, vintage (issue month or year), purpose, term, state, income, DTI, FICO score.
- **Simple profit:** we ignore fees and the company's own costs.
- **Data column names** (for example, the column for "principal paid back") are checked in Phase 2 and added here.
