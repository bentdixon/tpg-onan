# Forward vs Backward: Demo Report

- Forward model: `d16_fwd` (step 3584), next-token prediction: sees tokens to the **left**.
- Backward model: `d16_bwd` (step 3584), previous-token prediction: sees tokens to the **right**.
- Generation: 1 greedy + 3 samples (temperature 0.8, top-k 50, max 96 tokens, seed 42).
- Token tables are teacher-forced on the true passage. `␣` marks a space; Rank 1 means the model's top guess was correct.

## Summary

| # | Passage | Category | Tokens | Next-token bpb (fwd) | Prev-token bpb (bwd) | Next-token top-1 acc | Prev-token top-1 acc |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | [match_cancelled](#1-match-cancelled) | causal | 47 | 0.884 | 0.941 | 38% | 40% |
| 2 | [power_cut](#2-power-cut) | causal | 47 | 0.852 | 0.861 | 32% | 34% |
| 3 | [crop_failure](#3-crop-failure) | causal | 38 | 0.852 | 0.907 | 37% | 24% |
| 4 | [late_train](#4-late-train) | temporal | 49 | 0.934 | 1.004 | 43% | 39% |
| 5 | [bread_recipe](#5-bread-recipe) | temporal | 60 | 0.623 | 0.617 | 63% | 55% |
| 6 | [moon_landing](#6-moon-landing) | temporal | 51 | 0.658 | 0.628 | 57% | 57% |
| 7 | [socrates](#7-socrates) | logical | 20 | 0.907 | 0.770 | 55% | 45% |
| 8 | [even_numbers](#8-even-numbers) | logical | 58 | 0.767 | 0.734 | 47% | 47% |
| 9 | [water_boils](#9-water-boils) | logical | 48 | 0.625 | 0.658 | 46% | 44% |
| 10 | [detective](#10-detective) | logical | 52 | 1.028 | 1.085 | 44% | 37% |
| 11 | [lost_dog](#11-lost-dog) | narrative | 45 | 1.138 | 1.162 | 38% | 29% |
| 12 | [job_interview](#12-job-interview) | narrative | 39 | 0.994 | 1.044 | 36% | 36% |
| 13 | [photosynthesis](#13-photosynthesis) | factual | 44 | 0.452 | 0.453 | 61% | 57% |
| 14 | [python_function](#14-python-function) | factual | 52 | 0.692 | 0.782 | 54% | 48% |

Byte-weighted mean bpb on demo passages: forward **0.803**, backward **0.827** (+3.0%). Small sample; use `compare_bpb.sh` for the real comparison.

---

## 1. match_cancelled

*Category: causal*

> **Beginning:** Heavy rain fell on the stadium for most of Saturday afternoon.  
> **Middle:** By three o'clock the pitch was flooded and the referee declared it unsafe for the players.  
> **Ending:** So the match was cancelled and rescheduled for the following week.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | at the end of the match, he was knocked out at the end of the match, he was knocked out at the end of the match, he was knocked out at the end of the match, he was knocked out at the end of the match, he was knocked out at the end of the match, he was knocked out at the end of the match, he was knocked out at the end of the match, and he was knocked out at the end of the match. ↵  ↵ | So the match was cancelled and rescheduled for the following week. |
| sample | a list of plants that are toxic to dogs. ↵  ↵ Below is a list of plants that are toxic to dogs. A list of plants that are toxic to dogs. ↵  ↵ Why should bunnies not be given to dogs when they are so toxic? ↵  ↵ "Because they are toxic to dogs," said Ben Maynard. Maynard is a spokesperson for the American Kennel Club. He is a spokesperson for the American Kennel Association (AKA) on the day of the match. ↵  ↵ | So the match was cancelled and rescheduled for the following week. |
| sample | pandemic, the first 24 to 48 hours would have been moved back in increments of 24 to 48 hours to accommodate the huge number of people working from home. So if people were working from home, it would have been over 48 hours before being moved back in. ↵  ↵ We had our first match last week, and judging from the matches, there were only 3 matches last week. However, there were two good matches but these were gone after a few days. ↵ | So the match was cancelled and rescheduled for the following week. |
| sample | , so the number of players has also changed, and the game now has two players in it. ↵  ↵ The match was put off for a week? Three days? ↵  ↵ The match was close to the end of the match and was only put off for two to three days. ↵ Our team had started the match by the end of the week and was strong enough to pull it off. However, it was blacked out at the start of the night, changing the starting date for the match. ↵ | So the match was cancelled and rescheduled for the following week. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | Heavy rain fell on the stadium for most of Saturday afternoon. | The rain was so heavy that the stadium was flooded. The stadium was flooded for 2 hours. The stadium was flooded for 2 hours. The stadium was flooded for 2 hours. The stadium was flooded for 2 hours. The stadium was flooded for 2 hours. The stadium was flooded for 2 hours. The stadium was flooded for 2 hours. The stadium was flooded for 2 hours. The stadium was flooded for 2 hours. The stadium was flooded |
| sample | Heavy rain fell on the stadium for most of Saturday afternoon. | The rain is not a pleasant feeling when you try to stay inside without putting the roof on your head, even if the rain is a little more intense. Even though the rain was more intense than what happened during the day, I believe we should all be able to appreciate the beauty of the rain in all the different colors that it brought to the stadium. ↵ The rain in the stadium was not exactly pleasant to see, but we all know that we should be ready for the rainstorm |
| sample | Heavy rain fell on the stadium for most of Saturday afternoon. | Even at the end of the game, the fans all agreed that the Beretani is a terrible football team. The stadium was full of people so loud they could hear the game. Only the football field was completely empty. There was just two players on the field. They all kept saying that they were playing the right thing. The crowd, as well as the fans, began to change their minds. The Beretani is a new team and is not a threat |
| sample | Heavy rain fell on the stadium for most of Saturday afternoon. | It was over 140 degrees at the parking lot. As it came down, it was raining down 45 feet. The roof was covered in 100-degree rain and the pavement and the 6-foot white stripes at the parking lot were so thick it looked like a snowstorm came through the trees. When the 100-degree rain broke down the streets, it poured down the 18- and 19-foot-wide roof. Many people had to stand up |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.884 | 38% |
| Backward | previous-token (right context) | 0.941 | 40% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `He` | 0.001 | 148 | `The` 0.06, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | He → ? | `avy` | 0.108 | 1 | `avy` 0.11, `aling` 0.05, `␣was` 0.05, `␣is` 0.05, `ating` 0.04 |
| 3 | Heavy → ? | `␣rain` | 0.040 | 4 | `␣metals` 0.07, `␣metal` 0.07, `␣Metal` 0.06, `␣rain` 0.04, `␣rains` 0.04 |
| 4 | Heavy rain → ? | `␣fell` | 0.004 | 33 | `␣is` 0.09, `␣and` 0.09, `,` 0.07, `␣in` 0.06, `␣has` 0.05 |
| 5 | Heavy rain fell → ? | `␣on` | 0.221 | 1 | `␣on` 0.22, `␣in` 0.13, `␣over` 0.04, `␣for` 0.03, `␣across` 0.03 |
| 6 | …avy rain fell on → ? | `␣the` | 0.506 | 1 | `␣the` 0.51, `␣a` 0.03, `␣Friday` 0.02, `␣Wednesday` 0.02, `␣Monday` 0.02 |
| 7 | …rain fell on the → ? | `␣stadium` | 0.000 | 916 | `␣` 0.03, `␣island` 0.02, `␣city` 0.01, `␣roof` 0.01, `␣forest` 0.01 |
| 8 | …fell on the stadium → ? | `␣for` | 0.015 | 15 | `,` 0.11, `'s` 0.10, `␣on` 0.06, `␣in` 0.05, `␣and` 0.04 |
| 9 | …on the stadium for → ? | `␣most` | 0.016 | 13 | `␣the` 0.24, `␣a` 0.14, `␣` 0.08, `␣several` 0.04, `␣about` 0.04 |
| 10 | …the stadium for most → ? | `␣of` | 0.945 | 1 | `␣of` 0.94, `␣days` 0.01, `␣parts` 0.01, `␣games` 0.00, `␣nights` 0.00 |
| 11 | …stadium for most of → ? | `␣Saturday` | 0.005 | 11 | `␣the` 0.85, `␣August` 0.01, `␣this` 0.01, `␣March` 0.01, `␣last` 0.01 |
| 12 | …for most of Saturday → ? | `␣afternoon` | 0.053 | 6 | `,` 0.33, `.` 0.13, `␣night` 0.11, `␣morning` 0.10, `␣and` 0.09 |
| 13 | …most of Saturday afternoon → ? | `.` | 0.297 | 2 | `,` 0.38, `.` 0.30, `␣and` 0.08, `␣as` 0.02, `␣(` 0.02 |
| 14 | …of Saturday afternoon. → ? | `␣By` | 0.007 | 24 | `␣The` 0.18, `␣It` 0.06, `␣A` 0.03, `␣I` 0.02, `␣There` 0.02 |
| 15 | …Saturday afternoon. By → ? | `␣three` | 0.001 | 42 | `␣Sunday` 0.19, `␣the` 0.18, `␣` 0.18, `␣noon` 0.07, `␣mid` 0.04 |
| 16 | …afternoon. By three → ? | `␣o` | 0.314 | 1 | `␣o` 0.31, `␣p` 0.24, `␣a` 0.05, `,` 0.04, `␣in` 0.04 |
| 17 | …. By three o → ? | `'` | 0.982 | 1 | `'` 0.98, `␣clock` 0.01, `’` 0.00, `clock` 0.00, `.` 0.00 |
| 18 | …By three o' → ? | `clock` | 0.991 | 1 | `clock` 0.99, `␣clock` 0.01, `Cl` 0.00, `cl` 0.00, `'` 0.00 |
| 19 | …three o'clock → ? | `␣the` | 0.171 | 2 | `,` 0.32, `␣the` 0.17, `␣on` 0.10, `␣Sunday` 0.05, `␣in` 0.04 |
| 20 | …o'clock the → ? | `␣pitch` | 0.006 | 22 | `␣rain` 0.09, `␣stadium` 0.08, `␣sun` 0.05, `␣weather` 0.04, `␣wind` 0.04 |
| 21 | …'clock the pitch → ? | `␣was` | 0.281 | 1 | `␣was` 0.28, `␣had` 0.23, `ing` 0.06, `␣of` 0.03, `␣reached` 0.02 |
| 22 | …clock the pitch was → ? | `␣flooded` | 0.019 | 7 | `␣down` 0.05, `␣` 0.04, `␣up` 0.03, `␣still` 0.03, `␣dry` 0.02 |
| 23 | …the pitch was flooded → ? | `␣and` | 0.205 | 1 | `␣and` 0.20, `␣with` 0.17, `.` 0.17, `,` 0.16, `␣to` 0.05 |
| 24 | …pitch was flooded and → ? | `␣the` | 0.315 | 1 | `␣the` 0.32, `␣a` 0.05, `␣it` 0.03, `␣there` 0.03, `␣all` 0.02 |
| 25 | …was flooded and the → ? | `␣refere` | 0.002 | 51 | `␣stadium` 0.11, `␣crowd` 0.05, `␣pitch` 0.03, `␣game` 0.03, `␣fans` 0.02 |
| 26 | …flooded and the refere → ? | `e` | 0.681 | 1 | `e` 0.68, `es` 0.30, `nd` 0.01, `ed` 0.00, `ee` 0.00 |
| 27 | …and the referee → ? | `␣declared` | 0.007 | 18 | `␣was` 0.17, `␣had` 0.10, `'s` 0.08, `␣called` 0.05, `␣said` 0.02 |
| 28 | …the referee declared → ? | `␣it` | 0.080 | 4 | `␣the` 0.22, `␣a` 0.21, `␣that` 0.19, `␣it` 0.08, `␣an` 0.04 |
| 29 | …referee declared it → ? | `␣unsafe` | 0.014 | 9 | `␣a` 0.29, `␣was` 0.09, `␣to` 0.07, `␣"` 0.07, `␣an` 0.05 |
| 30 | …e declared it unsafe → ? | `␣for` | 0.203 | 3 | `␣to` 0.46, `.` 0.23, `␣for` 0.20, `.\n` 0.02, `␣and` 0.01 |
| 31 | …declared it unsafe for → ? | `␣the` | 0.231 | 1 | `␣the` 0.23, `␣play` 0.17, `␣use` 0.08, `␣a` 0.06, `␣playing` 0.04 |
| 32 | …it unsafe for the → ? | `␣players` | 0.036 | 4 | `␣game` 0.34, `␣team` 0.05, `␣fans` 0.04, `␣players` 0.04, `␣games` 0.03 |
| 33 | …unsafe for the players → ? | `.` | 0.250 | 2 | `␣to` 0.58, `.` 0.25, `.\n` 0.03, `␣and` 0.02, `,` 0.02 |
| 34 | …for the players. → ? | `␣So` | 0.004 | 37 | `␣The` 0.23, `␣He` 0.05, `␣It` 0.03, `␣A` 0.03, `␣As` 0.02 |
| 35 | …the players. So → ? | `␣the` | 0.216 | 1 | `␣the` 0.22, `,` 0.15, `␣he` 0.09, `␣they` 0.04, `on` 0.04 |
| 36 | …players. So the → ? | `␣match` | 0.002 | 61 | `␣refere` 0.10, `␣players` 0.07, `␣game` 0.06, `␣stadium` 0.04, `␣officials` 0.04 |
| 37 | …. So the match → ? | `␣was` | 0.529 | 1 | `␣was` 0.53, `␣began` 0.04, `␣started` 0.04, `␣ended` 0.04, `␣went` 0.04 |
| 38 | …So the match was → ? | `␣cancelled` | 0.095 | 2 | `␣over` 0.11, `␣cancelled` 0.09, `␣postp` 0.08, `␣hal` 0.05, `␣res` 0.04 |
| 39 | …the match was cancelled → ? | `␣and` | 0.149 | 2 | `.` 0.36, `␣and` 0.15, `.\n` 0.13, `,` 0.07, `.\n\n` 0.04 |
| 40 | …match was cancelled and → ? | `␣res` | 0.002 | 50 | `␣the` 0.41, `␣a` 0.06, `␣no` 0.02, `␣all` 0.02, `␣it` 0.02 |
| 41 | …was cancelled and res → ? | `ched` | 0.836 | 1 | `ched` 0.84, `umed` 0.13, `che` 0.01, `umes` 0.01, `uming` 0.00 |
| 42 | …cancelled and resched → ? | `uled` | 0.990 | 1 | `uled` 0.99, `uling` 0.01, `ules` 0.00, `ued` 0.00, `ored` 0.00 |
| 43 | …and rescheduled → ? | `␣for` | 0.382 | 1 | `␣for` 0.38, `␣to` 0.19, `.` 0.10, `.\n` 0.05, `␣on` 0.03 |
| 44 | …rescheduled for → ? | `␣the` | 0.183 | 2 | `␣Sunday` 0.25, `␣the` 0.18, `␣Saturday` 0.10, `␣next` 0.08, `␣a` 0.06 |
| 45 | …cheduled for the → ? | `␣following` | 0.135 | 2 | `␣next` 0.36, `␣following` 0.13, `␣weekend` 0.06, `␣Sunday` 0.04, `␣evening` 0.04 |
| 46 | …uled for the following → ? | `␣week` | 0.025 | 7 | `␣day` 0.32, `␣Sunday` 0.20, `␣Saturday` 0.15, `␣morning` 0.11, `␣weekend` 0.03 |
| 47 | …for the following week → ? | `.` | 0.474 | 1 | `.` 0.47, `.\n` 0.23, `.\n\n` 0.08, `,` 0.04, `␣with` 0.01 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.519 | 1 | `.` 0.52, `!` 0.03, `)` 0.02, `).` 0.01, `?` 0.01 |
| 2 | ? ← . | `␣week` | 0.001 | 76 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣Yes` 0.00, `␣years` 0.00 |
| 3 | ? ← week. | `␣following` | 0.011 | 11 | `␣a` 0.39, `␣per` 0.12, `␣the` 0.08, `␣this` 0.08, `␣next` 0.07 |
| 4 | ? ← following week. | `␣the` | 0.952 | 1 | `␣the` 0.95, `␣The` 0.04, `␣that` 0.00, `␣or` 0.00, `␣every` 0.00 |
| 5 | ? ← the following week. | `␣for` | 0.161 | 1 | `␣for` 0.16, `␣of` 0.08, `␣in` 0.07, `␣by` 0.04, `␣during` 0.03 |
| 6 | ? ← for the following week… | `uled` | 0.000 | 389 | `␣activities` 0.02, `␣plan` 0.02, `␣schedule` 0.01, `␣planned` 0.01, `␣plans` 0.01 |
| 7 | ? ← uled for the following… | `ched` | 0.818 | 1 | `ched` 0.82, `hed` 0.15, `␣overha` 0.01, `␣shed` 0.00, `␣ma` 0.00 |
| 8 | ? ← cheduled for the… | `␣res` | 0.893 | 1 | `␣res` 0.89, `-s` 0.08, `␣Res` 0.01, `res` 0.00, `S` 0.00 |
| 9 | ? ← rescheduled for… | `␣and` | 0.035 | 5 | `␣be` 0.60, `␣is` 0.09, `␣are` 0.05, `␣was` 0.04, `␣and` 0.04 |
| 10 | ? ← and rescheduled… | `␣cancelled` | 0.063 | 2 | `,` 0.08, `␣cancelled` 0.06, `␣day` 0.05, `␣week` 0.04, `uled` 0.03 |
| 11 | ? ← cancelled and resched… | `␣was` | 0.098 | 3 | `␣be` 0.58, `␣is` 0.10, `␣was` 0.10, `␣are` 0.04, `␣were` 0.03 |
| 12 | ? ← was cancelled and res… | `␣match` | 0.001 | 66 | `␣it` 0.10, `␣It` 0.09, `␣event` 0.08, `␣class` 0.06, `␣program` 0.05 |
| 13 | ? ← match was cancelled and… | `␣the` | 0.537 | 1 | `␣the` 0.54, `␣The` 0.30, `The` 0.01, `␣that` 0.01, `'s` 0.01 |
| 14 | ? ← the match was cancelled… | `␣So` | 0.002 | 20 | `,` 0.57, `␣and` 0.10, `␣but` 0.06, `␣that` 0.04, `␣so` 0.03 |
| 15 | ? ← So the match was… | `.` | 0.905 | 1 | `.` 0.90, `).` 0.01, `:` 0.01, `!` 0.01, `."` 0.01 |
| 16 | ? ← . So the match… | `␣players` | 0.002 | 44 | `␣match` 0.04, `␣time` 0.02, `␣matches` 0.01, `␣it` 0.01, `␣week` 0.01 |
| 17 | ? ← players. So the… | `␣the` | 0.189 | 1 | `␣the` 0.19, `␣other` 0.09, `␣of` 0.04, `␣two` 0.03, `␣young` 0.01 |
| 18 | ? ← the players. So… | `␣for` | 0.158 | 2 | `␣of` 0.24, `␣for` 0.16, `␣to` 0.11, `␣between` 0.05, `␣by` 0.05 |
| 19 | ? ← for the players.… | `␣unsafe` | 0.001 | 137 | `␣match` 0.03, `␣difficult` 0.02, `␣problems` 0.02, `␣frustrating` 0.02, `␣game` 0.02 |
| 20 | ? ← unsafe for the players… | `␣it` | 0.086 | 3 | `␣and` 0.17, `␣was` 0.17, `␣it` 0.09, `␣very` 0.07, `␣too` 0.05 |
| 21 | ? ← it unsafe for the… | `␣declared` | 0.009 | 7 | `␣making` 0.43, `␣made` 0.35, `␣make` 0.11, `␣found` 0.02, `␣deemed` 0.01 |
| 22 | ? ← declared it unsafe for… | `e` | 0.002 | 51 | `␣and` 0.34, `␣they` 0.03, `␣had` 0.03, `␣officials` 0.03, `␣who` 0.02 |
| 23 | ? ← e declared it unsafe… | `␣refere` | 0.888 | 1 | `␣refere` 0.89, `ere` 0.05, `we` 0.01, `ine` 0.00, `ore` 0.00 |
| 24 | ? ← referee declared it… | `␣the` | 0.794 | 1 | `␣the` 0.79, `␣The` 0.11, `The` 0.01, `␣a` 0.01, `␣match` 0.01 |
| 25 | ? ← the referee declared… | `␣and` | 0.223 | 2 | `,` 0.26, `␣and` 0.22, `␣but` 0.15, `␣after` 0.04, `␣as` 0.04 |
| 26 | ? ← and the referee… | `␣flooded` | 0.000 | 834 | `,` 0.24, `␣match` 0.07, `␣game` 0.02, `␣matches` 0.01, `␣time` 0.01 |
| 27 | ? ← flooded and the refere… | `␣was` | 0.577 | 1 | `␣was` 0.58, `␣got` 0.05, `␣were` 0.04, `␣completely` 0.03, `␣became` 0.02 |
| 28 | ? ← was flooded and the… | `␣pitch` | 0.035 | 5 | `␣stadium` 0.20, `␣field` 0.13, `␣match` 0.09, `adium` 0.06, `␣pitch` 0.04 |
| 29 | ? ← pitch was flooded and… | `␣the` | 0.670 | 1 | `␣the` 0.67, `␣The` 0.22, `The` 0.02, `␣cricket` 0.01, `␣football` 0.01 |
| 30 | ? ← the pitch was flooded… | `clock` | 0.000 | 2282 | `,` 0.43, `␣when` 0.07, `␣but` 0.04, `␣that` 0.04, `␣because` 0.04 |
| 31 | ? ← clock the pitch was… | `'` | 0.919 | 1 | `'` 0.92, `’` 0.03, `␣o` 0.02, `00` 0.01, `.` 0.00 |
| 32 | ? ← 'clock the pitch… | `␣o` | 0.969 | 1 | `␣o` 0.97, `o` 0.01, `0` 0.01, `␣O` 0.00, `-o` 0.00 |
| 33 | ? ← o'clock the… | `␣three` | 0.028 | 13 | `10` 0.08, `11` 0.07, `3` 0.07, `6` 0.07, `9` 0.05 |
| 34 | ? ← three o'clock… | `␣By` | 0.056 | 7 | `␣at` 0.18, `␣At` 0.14, `␣around` 0.13, `␣after` 0.08, `␣by` 0.07 |
| 35 | ? ← By three o'… | `.` | 0.933 | 1 | `.` 0.93, `).` 0.02, `:` 0.01, `'.` 0.01, `!` 0.00 |
| 36 | ? ← . By three o… | `␣afternoon` | 0.005 | 18 | `␣match` 0.03, `␣pitch` 0.03, `␣game` 0.02, `␣minutes` 0.02, `clock` 0.02 |
| 37 | ? ← afternoon. By three… | `␣Saturday` | 0.040 | 5 | `␣the` 0.38, `␣that` 0.20, `␣late` 0.06, `␣Sunday` 0.04, `␣Saturday` 0.04 |
| 38 | ? ← Saturday afternoon. By… | `␣of` | 0.018 | 5 | `␣on` 0.55, `␣a` 0.11, `␣the` 0.04, `␣that` 0.02, `␣of` 0.02 |
| 39 | ? ← of Saturday afternoon.… | `␣most` | 0.027 | 9 | `␣hours` 0.14, `␣morning` 0.11, `␣as` 0.08, `␣afternoon` 0.07, `␣middle` 0.07 |
| 40 | ? ← most of Saturday afternoon… | `␣for` | 0.431 | 1 | `␣for` 0.43, `␣during` 0.06, `␣lasted` 0.03, `␣throughout` 0.03, `␣through` 0.03 |
| 41 | ? ← for most of Saturday… | `␣stadium` | 0.002 | 88 | `␣pitch` 0.05, `␣rain` 0.03, `␣played` 0.02, `ed` 0.02, `␣on` 0.02 |
| 42 | ? ← stadium for most of… | `␣the` | 0.803 | 1 | `␣the` 0.80, `␣home` 0.01, `␣main` 0.01, `␣football` 0.00, `'s` 0.00 |
| 43 | ? ← the stadium for most… | `␣on` | 0.003 | 24 | `␣in` 0.35, `␣at` 0.15, `␣of` 0.09, `␣inside` 0.04, `␣around` 0.04 |
| 44 | ? ← on the stadium for… | `␣fell` | 0.060 | 3 | `␣rain` 0.14, `␣descended` 0.09, `␣fell` 0.06, `␣down` 0.06, `ined` 0.02 |
| 45 | ? ← fell on the stadium… | `␣rain` | 0.769 | 1 | `␣rain` 0.77, `␣snow` 0.05, `␣Rain` 0.03, `␣rains` 0.01, `␣darkness` 0.01 |
| 46 | ? ← rain fell on the… | `avy` | 0.034 | 7 | `␣heavy` 0.29, `␣of` 0.13, `␣and` 0.10, `␣Heavy` 0.08, `ial` 0.07 |
| 47 | ? ← avy rain fell on… | `He` | 0.988 | 1 | `He` 0.99, `he` 0.01, `-he` 0.00, `␣He` 0.00, `She` 0.00 |

---

## 2. power_cut

*Category: causal*

> **Beginning:** A storm brought down several power lines on the edge of town last night.  
> **Middle:** Thousands of homes lost electricity, and traffic lights across the city stopped working.  
> **Ending:** As a result, schools stayed closed the next morning while engineers repaired the damage.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | it, we didn't know what to do about it, we didn't know what to do about it, we didn't know what to do about it, we didn't know what to do about it, we didn't know what to do about it, we didn't know what to do about it, we didn't know what to do about it, we didn't know what to do about it, and we didn't know what to do about it," he said. ↵  ↵ | As a result, schools stayed closed the next morning while engineers repaired the damage. |
| sample | people that this is one way to mitigate the damage to schools. We wanted to be ready to go as quickly as possible to repair the damage done while the school was open," Bronson said. ↵  ↵ Because the schools are closed for 24 hours every day, the schools stayed closed, and this continued for several days. They never called for help. "There is no relief to schools, teachers, or any of those who were touched by the damage," Bronson said. ↵  ↵ | As a result, schools stayed closed the next morning while engineers repaired the damage. |
| sample | , the power did not go out until the next morning. ↵ As a result, the building did not have electricity until the next morning. ↵ As a result, many died. Some of the deaths were related to the plumbing problems, such as frozen pipes. ↵ As a result, engineers shut off the water in the building, and cut off water pipes from the system. ↵ Others were returned to the building, and consisted of pipes, hoses, water line and other parts of the system. ↵ | As a result, schools stayed closed the next morning while engineers repaired the damage. |
| sample | deal with thousands of students in a day, officials said. ↵ At this high school, the authorities decided to conduct an attack on the high school. They have asked the school authorities to shut the high schools, and they have given relief to the students in school blocks that were on the grounds of the school, officials said. ↵ They have also allowed high school students and other students to go back to the public schools that had previously been closed since the schools were closed, the government said. ↵ | As a result, schools stayed closed the next morning while engineers repaired the damage. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | A storm brought down several power lines on the edge of town last night. | The power lines were damaged and the power company was forced to shut down the power lines. The power company was forced to shut down the power lines because they were damaged. The power company was forced to shut down the power lines because they were damaged. The power company was forced to shut down the power lines because they were damaged. The power company was forced to shut down the power lines because they were damaged. The power company was forced to shut down the power lines because they were |
| sample | A storm brought down several power lines on the edge of town last night. | The power is still on, and so is the water. But one incident, in the vicinity of Lake Winnipeg, is quite unfortunate. ↵ When storm water was first discovered in the area in 1889, it was blamed for the flooding of the town. But the water was not caused by rainfall, but by a storm. That was until a few years later, when a landslide in 2013 left an area of land in the Lake Winnipeg |
| sample | A storm brought down several power lines on the edge of town last night. | People evacuated their homes and cars from the town by climbing up to the edge of town. A huge amount of power was lost, but everyone stayed safe. We are still at 100% power in the area, but it has gone dark and we are still being asked to pay for power. We have been going out of town and I just want to remind everyone of how important it is to be prepared. ↵ No, the storm was not a hurricane, but a meteor |
| sample | A storm brought down several power lines on the edge of town last night. | It was too strong to operate a water pump. ↵  ↵ The power outages lasted 30 minutes. The power company said they had to shut down the power lines to reduce the risk of a power outage. ↵  ↵ But the power company said the outage didn't last long. If the storm continues, they say, those power lines might be at risk of being damaged. ↵  ↵ The power company said they have to shut down the power lines on the edge of town because power lines are subject to outages that can |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.852 | 32% |
| Backward | previous-token (right context) | 0.861 | 34% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `A` | 0.021 | 5 | `The` 0.06, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | A → ? | `␣storm` | 0.000 | 1658 | `␣new` 0.03, `:` 0.02, `␣few` 0.02, `␣` 0.01, `␣Guide` 0.01 |
| 3 | A storm → ? | `␣brought` | 0.001 | 138 | `␣is` 0.14, `␣surge` 0.08, `y` 0.06, `␣of` 0.05, `␣that` 0.03 |
| 4 | A storm brought → ? | `␣down` | 0.050 | 3 | `␣a` 0.09, `␣the` 0.07, `␣down` 0.05, `␣heavy` 0.05, `␣in` 0.03 |
| 5 | A storm brought down → ? | `␣several` | 0.020 | 7 | `␣a` 0.26, `␣the` 0.13, `␣` 0.11, `␣an` 0.04, `␣two` 0.03 |
| 6 | …storm brought down several → ? | `␣power` | 0.011 | 13 | `␣trees` 0.09, `␣buildings` 0.04, `␣hundred` 0.04, `␣people` 0.03, `␣thousand` 0.03 |
| 7 | …brought down several power → ? | `␣lines` | 0.506 | 1 | `␣lines` 0.51, `␣poles` 0.10, `␣plants` 0.09, `␣outages` 0.07, `lines` 0.04 |
| 8 | …down several power lines → ? | `␣on` | 0.030 | 8 | `␣in` 0.25, `␣and` 0.16, `,` 0.13, `␣across` 0.05, `␣at` 0.04 |
| 9 | …several power lines on → ? | `␣the` | 0.332 | 1 | `␣the` 0.33, `␣a` 0.06, `␣my` 0.02, `␣Saturday` 0.02, `␣Friday` 0.02 |
| 10 | …power lines on the → ? | `␣edge` | 0.003 | 68 | `␣East` 0.02, `␣east` 0.02, `␣` 0.02, `␣island` 0.02, `␣coast` 0.02 |
| 11 | …lines on the edge → ? | `␣of` | 0.996 | 1 | `␣of` 1.00, `,` 0.00, `␣and` 0.00, `.` 0.00, `\n` 0.00 |
| 12 | …on the edge of → ? | `␣town` | 0.014 | 5 | `␣the` 0.32, `␣a` 0.08, `␣Lake` 0.04, `␣downtown` 0.02, `␣town` 0.01 |
| 13 | …the edge of town → ? | `␣last` | 0.028 | 5 | `,` 0.26, `.` 0.20, `␣in` 0.13, `␣and` 0.07, `␣on` 0.03 |
| 14 | …edge of town last → ? | `␣night` | 0.055 | 3 | `␣week` 0.48, `␣weekend` 0.12, `␣night` 0.05, `␣month` 0.05, `␣Friday` 0.04 |
| 15 | …of town last night → ? | `.` | 0.371 | 2 | `,` 0.40, `.` 0.37, `␣and` 0.04, `␣in` 0.04, `.\n` 0.01 |
| 16 | …town last night. → ? | `␣Th` | 0.003 | 63 | `␣The` 0.16, `␣It` 0.05, `␣A` 0.04, `␣In` 0.03, `␣I` 0.02 |
| 17 | …last night. Th → ? | `ousands` | 0.635 | 1 | `ousands` 0.63, `underst` 0.16, `irty` 0.08, `ir` 0.04, `ur` 0.01 |
| 18 | …night. Thousands → ? | `␣of` | 0.836 | 1 | `␣of` 0.84, `␣were` 0.05, `␣have` 0.02, `␣are` 0.01, `␣lost` 0.01 |
| 19 | …. Thousands of → ? | `␣homes` | 0.077 | 2 | `␣people` 0.50, `␣homes` 0.08, `␣residents` 0.05, `␣trees` 0.04, `␣power` 0.03 |
| 20 | …Thousands of homes → ? | `␣lost` | 0.021 | 8 | `␣were` 0.35, `␣and` 0.24, `␣in` 0.08, `,` 0.07, `␣across` 0.05 |
| 21 | …ousands of homes lost → ? | `␣electricity` | 0.089 | 2 | `␣power` 0.78, `␣electricity` 0.09, `␣their` 0.06, `␣electrical` 0.01, `␣internet` 0.01 |
| 22 | …of homes lost electricity → ? | `,` | 0.256 | 1 | `,` 0.26, `␣and` 0.19, `.` 0.19, `␣in` 0.06, `␣as` 0.03 |
| 23 | …homes lost electricity, → ? | `␣and` | 0.368 | 1 | `␣and` 0.37, `␣including` 0.03, `␣as` 0.02, `␣gas` 0.02, `␣many` 0.02 |
| 24 | …lost electricity, and → ? | `␣traffic` | 0.000 | 257 | `␣many` 0.07, `␣the` 0.07, `␣hundreds` 0.06, `␣thousands` 0.05, `␣a` 0.04 |
| 25 | …electricity, and traffic → ? | `␣lights` | 0.029 | 7 | `␣was` 0.22, `␣jams` 0.14, `␣congestion` 0.04, `␣jam` 0.03, `␣stopped` 0.03 |
| 26 | …, and traffic lights → ? | `␣across` | 0.014 | 12 | `␣were` 0.34, `␣and` 0.07, `␣went` 0.05, `␣in` 0.05, `␣on` 0.03 |
| 27 | …and traffic lights across → ? | `␣the` | 0.604 | 1 | `␣the` 0.60, `␣town` 0.16, `␣New` 0.01, `␣a` 0.01, `␣our` 0.01 |
| 28 | …traffic lights across the → ? | `␣city` | 0.157 | 2 | `␣country` 0.18, `␣city` 0.16, `␣road` 0.12, `␣street` 0.11, `␣town` 0.07 |
| 29 | …lights across the city → ? | `␣stopped` | 0.010 | 8 | `␣were` 0.50, `␣went` 0.04, `␣have` 0.02, `␣bl` 0.02, `␣collapsed` 0.02 |
| 30 | …across the city stopped → ? | `␣working` | 0.661 | 1 | `␣working` 0.66, `.` 0.06, `␣functioning` 0.04, `␣flashing` 0.03, `␣work` 0.02 |
| 31 | …the city stopped working → ? | `.` | 0.554 | 1 | `.` 0.55, `.\n` 0.07, `␣for` 0.05, `.\n\n` 0.04, `,` 0.04 |
| 32 | …city stopped working. → ? | `␣As` | 0.020 | 6 | `␣The` 0.13, `␣A` 0.05, `␣But` 0.05, `␣It` 0.03, `␣In` 0.03 |
| 33 | …stopped working. As → ? | `␣a` | 0.163 | 2 | `␣the` 0.24, `␣a` 0.16, `␣of` 0.05, `␣many` 0.03, `␣people` 0.03 |
| 34 | …working. As a → ? | `␣result` | 0.719 | 1 | `␣result` 0.72, `␣consequence` 0.02, `␣homeowner` 0.01, `␣reminder` 0.01, `␣matter` 0.01 |
| 35 | …. As a result → ? | `,` | 0.916 | 1 | `,` 0.92, `␣of` 0.07, `␣the` 0.00, `␣many` 0.00, `␣there` 0.00 |
| 36 | …As a result, → ? | `␣schools` | 0.005 | 30 | `␣the` 0.14, `␣many` 0.09, `␣a` 0.06, `␣` 0.03, `␣several` 0.03 |
| 37 | …a result, schools → ? | `␣stayed` | 0.001 | 43 | `␣and` 0.21, `␣were` 0.21, `␣closed` 0.15, `,` 0.12, `␣across` 0.06 |
| 38 | …result, schools stayed → ? | `␣closed` | 0.526 | 1 | `␣closed` 0.53, `␣open` 0.42, `␣shut` 0.02, `␣on` 0.00, `␣in` 0.00 |
| 39 | …, schools stayed closed → ? | `␣the` | 0.002 | 25 | `,` 0.31, `␣for` 0.20, `␣and` 0.11, `.` 0.11, `␣until` 0.08 |
| 40 | …schools stayed closed the → ? | `␣next` | 0.137 | 3 | `␣night` 0.26, `␣entire` 0.22, `␣next` 0.14, `␣rest` 0.12, `␣whole` 0.08 |
| 41 | …stayed closed the next → ? | `␣morning` | 0.113 | 2 | `␣day` 0.83, `␣morning` 0.11, `␣few` 0.02, `␣night` 0.01, `␣week` 0.01 |
| 42 | …closed the next morning → ? | `␣while` | 0.006 | 13 | `.` 0.32, `,` 0.29, `␣and` 0.07, `.\n` 0.06, `.\n\n` 0.05 |
| 43 | …the next morning while → ? | `␣engineers` | 0.001 | 184 | `␣the` 0.13, `␣many` 0.03, `␣police` 0.03, `␣people` 0.03, `␣students` 0.02 |
| 44 | …next morning while engineers → ? | `␣repaired` | 0.013 | 10 | `␣worked` 0.15, `␣and` 0.08, `␣were` 0.07, `␣tried` 0.03, `␣scrambled` 0.02 |
| 45 | …morning while engineers repaired → ? | `␣the` | 0.281 | 1 | `␣the` 0.28, `␣power` 0.06, `␣broken` 0.06, `␣and` 0.06, `␣many` 0.03 |
| 46 | …while engineers repaired the → ? | `␣damage` | 0.107 | 2 | `␣power` 0.18, `␣damage` 0.11, `␣damaged` 0.09, `␣broken` 0.08, `␣lines` 0.03 |
| 47 | …engineers repaired the damage → ? | `.` | 0.388 | 1 | `.` 0.39, `.\n` 0.17, `␣to` 0.14, `.\n\n` 0.10, `␣and` 0.05 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.519 | 1 | `.` 0.52, `!` 0.03, `)` 0.02, `).` 0.01, `?` 0.01 |
| 2 | ? ← . | `␣damage` | 0.001 | 115 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣Yes` 0.00, `␣years` 0.00 |
| 3 | ? ← damage. | `␣the` | 0.032 | 8 | `␣further` 0.06, `␣or` 0.05, `␣water` 0.04, `␣cause` 0.03, `␣of` 0.03 |
| 4 | ? ← the damage. | `␣repaired` | 0.001 | 96 | `␣of` 0.25, `␣repair` 0.12, `␣assess` 0.04, `␣fix` 0.03, `␣repairing` 0.03 |
| 5 | ? ← repaired the damage. | `␣engineers` | 0.000 | 142 | `␣and` 0.22, `␣have` 0.18, `␣has` 0.06, `␣successfully` 0.05, `␣that` 0.04 |
| 6 | ? ← engineers repaired the damage… | `␣while` | 0.012 | 11 | `␣the` 0.25, `␣and` 0.07, `␣The` 0.05, `␣until` 0.04, `'s` 0.04 |
| 7 | ? ← while engineers repaired the… | `␣morning` | 0.000 | 450 | `,` 0.15, `␣hours` 0.02, `␣days` 0.02, `␣minutes` 0.01, `␣weeks` 0.01 |
| 8 | ? ← morning while engineers repaired… | `␣next` | 0.129 | 2 | `␣the` 0.37, `␣next` 0.13, `␣this` 0.07, `␣following` 0.05, `␣Monday` 0.04 |
| 9 | ? ← next morning while engineers… | `␣the` | 0.931 | 1 | `␣the` 0.93, `␣until` 0.01, `␣early` 0.01, `␣The` 0.00, `␣very` 0.00 |
| 10 | ? ← the next morning while… | `␣closed` | 0.011 | 14 | `␣until` 0.06, `␣work` 0.03, `␣up` 0.02, `␣died` 0.02, `␣in` 0.02 |
| 11 | ? ← closed the next morning… | `␣stayed` | 0.006 | 14 | `␣was` 0.20, `␣were` 0.15, `␣be` 0.10, `␣and` 0.06, `␣factory` 0.02 |
| 12 | ? ← stayed closed the next… | `␣schools` | 0.004 | 38 | `␣and` 0.11, `␣They` 0.05, `␣It` 0.04, `␣it` 0.03, `␣they` 0.03 |
| 13 | ? ← schools stayed closed the… | `,` | 0.073 | 4 | `␣The` 0.19, `␣the` 0.16, `␣and` 0.10, `,` 0.07, `␣Most` 0.03 |
| 14 | ? ← , schools stayed closed… | `␣result` | 0.005 | 15 | `␣No` 0.06, `␣Yes` 0.03, `␣cases` 0.03, `␣However` 0.02, `␣case` 0.02 |
| 15 | ? ← result, schools stayed… | `␣a` | 0.984 | 1 | `␣a` 0.98, `␣the` 0.00, `␣that` 0.00, `␣as` 0.00, `␣this` 0.00 |
| 16 | ? ← a result, schools… | `␣As` | 0.841 | 1 | `␣As` 0.84, `␣as` 0.11, `As` 0.05, `as` 0.00, `␣was` 0.00 |
| 17 | ? ← As a result,… | `.` | 0.968 | 1 | `.` 0.97, `."` 0.01, `).` 0.01, `:` 0.00, `!` 0.00 |
| 18 | ? ← . As a result… | `␣working` | 0.000 | 322 | `␣schools` 0.02, `␣damage` 0.02, `␣school` 0.02, `␣it` 0.01, `␣night` 0.01 |
| 19 | ? ← working. As a… | `␣stopped` | 0.210 | 1 | `␣stopped` 0.21, `␣not` 0.11, `␣stop` 0.10, `'t` 0.07, `␣were` 0.07 |
| 20 | ? ← stopped working. As… | `␣city` | 0.000 | 400 | `␣had` 0.07, `␣and` 0.05, `␣schools` 0.04, `␣system` 0.03, `␣they` 0.03 |
| 21 | ? ← city stopped working.… | `␣the` | 0.812 | 1 | `␣the` 0.81, `␣entire` 0.07, `␣whole` 0.02, `␣a` 0.00, `␣capital` 0.00 |
| 22 | ? ← the city stopped working… | `␣across` | 0.084 | 3 | `␣in` 0.46, `␣of` 0.14, `␣across` 0.08, `␣throughout` 0.08, `␣to` 0.04 |
| 23 | ? ← across the city stopped… | `␣lights` | 0.016 | 6 | `␣schools` 0.46, `␣Schools` 0.03, `␣systems` 0.03, `␣buildings` 0.02, `␣lines` 0.02 |
| 24 | ? ← lights across the city… | `␣traffic` | 0.188 | 1 | `␣traffic` 0.19, `␣street` 0.18, `␣the` 0.13, `␣electric` 0.04, `␣and` 0.03 |
| 25 | ? ← traffic lights across the… | `␣and` | 0.168 | 2 | `␣the` 0.20, `␣and` 0.17, `,` 0.15, `␣all` 0.07, `␣of` 0.04 |
| 26 | ? ← and traffic lights across… | `,` | 0.289 | 1 | `,` 0.29, `␣schools` 0.05, `␣signs` 0.02, `␣school` 0.02, `␣roads` 0.01 |
| 27 | ? ← , and traffic lights… | `␣electricity` | 0.008 | 15 | `␣schools` 0.03, `␣closed` 0.03, `␣down` 0.02, `␣school` 0.01, `ed` 0.01 |
| 28 | ? ← electricity, and traffic… | `␣lost` | 0.072 | 4 | `␣no` 0.18, `␣without` 0.15, `␣of` 0.15, `␣lost` 0.07, `,` 0.07 |
| 29 | ? ← lost electricity, and… | `␣homes` | 0.022 | 7 | `␣schools` 0.13, `␣city` 0.06, `,` 0.04, `␣buildings` 0.04, `␣businesses` 0.03 |
| 30 | ? ← homes lost electricity,… | `␣of` | 0.092 | 3 | `,` 0.44, `0` 0.11, `␣of` 0.09, `␣Many` 0.05, `␣many` 0.04 |
| 31 | ? ← of homes lost electricity… | `ousands` | 0.215 | 2 | `␣thousands` 0.29, `ousands` 0.21, `undreds` 0.11, `␣hundreds` 0.11, `␣millions` 0.09 |
| 32 | ? ← ousands of homes lost… | `␣Th` | 0.949 | 1 | `␣Th` 0.95, `Th` 0.05, `th` 0.00, `-th` 0.00, `␣TH` 0.00 |
| 33 | ? ← Thousands of homes… | `.` | 0.963 | 1 | `.` 0.96, `:` 0.02, `."` 0.00, `).` 0.00, `!` 0.00 |
| 34 | ? ← . Thousands of… | `␣night` | 0.013 | 4 | `␣city` 0.02, `␣damage` 0.02, `␣power` 0.02, `␣night` 0.01, `␣down` 0.01 |
| 35 | ? ← night. Thousands… | `␣last` | 0.017 | 7 | `␣the` 0.25, `␣at` 0.21, `␣that` 0.16, `␣one` 0.06, `␣Monday` 0.03 |
| 36 | ? ← last night. Th… | `␣town` | 0.012 | 11 | `␣city` 0.04, `␣late` 0.03, `␣occurred` 0.02, `␣happened` 0.02, `␣struck` 0.02 |
| 37 | ? ← town last night.… | `␣of` | 0.060 | 3 | `␣the` 0.27, `␣in` 0.09, `␣of` 0.06, `␣to` 0.04, `␣through` 0.03 |
| 38 | ? ← of town last night… | `␣edge` | 0.018 | 11 | `␣part` 0.23, `␣out` 0.18, `␣parts` 0.08, `␣middle` 0.08, `␣center` 0.05 |
| 39 | ? ← edge of town last… | `␣the` | 0.893 | 1 | `␣the` 0.89, `␣eastern` 0.02, `␣southern` 0.02, `␣western` 0.02, `␣northern` 0.02 |
| 40 | ? ← the edge of town… | `␣on` | 0.405 | 1 | `␣on` 0.41, `␣at` 0.32, `␣to` 0.09, `␣along` 0.04, `␣near` 0.02 |
| 41 | ? ← on the edge of… | `␣lines` | 0.002 | 85 | `␣down` 0.04, `␣lights` 0.03, `␣occurred` 0.03, `␣outage` 0.02, `␣stranded` 0.02 |
| 42 | ? ← lines on the edge… | `␣power` | 0.729 | 1 | `␣power` 0.73, `␣electrical` 0.04, `␣electric` 0.03, `␣electricity` 0.02, `␣gas` 0.02 |
| 43 | ? ← power lines on the… | `␣several` | 0.006 | 25 | `␣the` 0.14, `␣down` 0.12, `ed` 0.06, `␣of` 0.05, `␣damaged` 0.05 |
| 44 | ? ← several power lines on… | `␣down` | 0.192 | 1 | `␣down` 0.19, `␣damaged` 0.08, `␣struck` 0.07, `ed` 0.06, `␣broke` 0.05 |
| 45 | ? ← down several power lines… | `␣brought` | 0.056 | 5 | `␣knocked` 0.34, `␣blew` 0.14, `re` 0.13, `␣shut` 0.10, `␣brought` 0.06 |
| 46 | ? ← brought down several power… | `␣storm` | 0.184 | 1 | `␣storm` 0.18, `␣that` 0.06, `storm` 0.05, `␣winds` 0.05, `␣tornado` 0.05 |
| 47 | ? ← storm brought down several… | `A` | 0.106 | 2 | `␣a` 0.11, `A` 0.11, `␣severe` 0.09, `␣A` 0.07, `␣ice` 0.06 |

---

## 3. crop_failure

*Category: causal*

> **Beginning:** The region received almost no rain between March and August.  
> **Middle:** Wells dried up and farmers could not irrigate their fields.  
> **Ending:** Because of the drought, the wheat harvest was the smallest in forty years.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | years of the drought, farmers harvested more than 1.5 million tons of wheat because of the drought. ↵ During the first two years of the drought, farmers harvested more than 1.5 million tons of wheat because of the drought. ↵ During the first two years of the drought, farmers harvested more than 1.5 million tons of wheat because of the drought. ↵ During the first two years of the drought, farmers harvested more than 1.5 million tons of wheat. ↵ | Because of the drought, the wheat harvest was the smallest in forty years. |
| sample | than a million acres. In forty years, farmers planted more than 300,000 acres of wheat. This year was the driest in forty years. ↵ The problem of growing wheat crops in California is worse today than it was forty years ago. The researchers estimate that the yields increased by more than 30 million gallons a year. ↵ California was not able to grow much wheat earlier this year, so farmers switched to other crops. This was the worst year of harvesting wheat. ↵ | Because of the drought, the wheat harvest was the smallest in forty years. |
| sample | 9, 2019, totalling more than 120,000 hectares in that time. ↵  ↵ The total wheat harvest fell in about 130,000 hectares during the drought, totalling more than 140,000 hectares on July 12, 2019. ↵  ↵ During the drought, wheat harvesters have damaged more than 130,000 hectares in the last 15 years, totalling more than 500,000 hectares. ↵  ↵ | Because of the drought, the wheat harvest was the smallest in forty years. |
| sample | component of the global carbon cycle that absorbs and traps large amounts of heat, contributing to the increases in atmospheric carbon dioxide. ↵  ↵ Wheat production does not release much carbon dioxide (CO2), a factor that could account for the drastic changes in Earth's climate over the past eight thousand years. ↵  ↵ Fun Facts ↵  ↵ Today, India is the world's largest producer of wheat. ↵  ↵ Large-scale commercial cultivation of wheat began in the 1920s, when 7.8 million people grew wheat. ↵  ↵ | Because of the drought, the wheat harvest was the smallest in forty years. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | The region received almost no rain between March and August. | The average temperature was 23.5°C (73.2°F) in the month of March, and the highest temperature was recorded in the month of August at 24.5°C (75.2°F). The average relative humidity was 72%. ↵ The month with the highest number of days with rain was March, with 11 days and 7 hours of sunshine. The month with the lowest number of days with rain was March, with 7 days and 6 |
| sample | The region received almost no rain between March and August. | The average temperatures were about 30 degrees but with a few exceptions: During January, February and March there were 5 to 10 days of snow with 15 to 20 inches of snow fall and the mean annual temperature of the city was 35 degrees. In April, May and June this temperature rarely exceeded 30 degrees. The month of July saw 14 to 20 days of snow, and 14 to 20 days of rain. However, in February the |
| sample | The region received almost no rain between March and August. | In October, the area received a wetter period until about mid-December with the highest rainfall recorded until January 2004. In November, the Met Office forecast that the Met Office would develop a second wetter period, in November, as this is the time when the rainiest seasons are. In September, the Met Office forecast that this period would be the wettest for 2018. The Met Office is forecast to develop an extreme wetter period between September and May |
| sample | The region received almost no rain between March and August. | In the late afternoon, most of the rain in the region occurred between 10 a.m. and 4 a.m. The rain fell in the low pressure zone of the low-pressure system which caused the lowest surface pressure (cp) to fall between 24.0 and 24.0 mmHg. Rainfall on the high pressure zone was very frequent throughout the region. ↵ The largest rainfall event occurs on the high pressure zone at 00:30. A total |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.852 | 37% |
| Backward | previous-token (right context) | 0.907 | 24% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `The` | 0.057 | 1 | `The` 0.06, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | The → ? | `␣region` | 0.000 | 2203 | `␣` 0.02, `␣first` 0.01, `␣Importance` 0.01, `␣most` 0.01, `␣best` 0.01 |
| 3 | The region → ? | `␣received` | 0.000 | 164 | `␣of` 0.19, `␣is` 0.16, `'s` 0.10, `␣has` 0.06, `␣was` 0.04 |
| 4 | The region received → ? | `␣almost` | 0.006 | 24 | `␣a` 0.18, `␣` 0.13, `␣the` 0.07, `␣an` 0.05, `␣more` 0.04 |
| 5 | The region received almost → ? | `␣no` | 0.161 | 2 | `␣` 0.37, `␣no` 0.16, `␣all` 0.07, `␣a` 0.06, `␣half` 0.04 |
| 6 | …region received almost no → ? | `␣rain` | 0.122 | 2 | `␣rainfall` 0.22, `␣rain` 0.12, `␣precipitation` 0.07, `␣attention` 0.04, `␣reports` 0.03 |
| 7 | …received almost no rain → ? | `␣between` | 0.016 | 14 | `␣in` 0.20, `␣for` 0.14, `␣during` 0.12, `,` 0.08, `␣this` 0.05 |
| 8 | …almost no rain between → ? | `␣March` | 0.037 | 10 | `␣` 0.34, `␣the` 0.08, `␣June` 0.05, `␣January` 0.05, `␣May` 0.05 |
| 9 | …no rain between March → ? | `␣and` | 0.435 | 2 | `␣` 0.54, `␣and` 0.44, `-A` 0.00, `,` 0.00, `␣to` 0.00 |
| 10 | …rain between March and → ? | `␣August` | 0.041 | 7 | `␣May` 0.35, `␣June` 0.17, `␣April` 0.10, `␣October` 0.09, `␣September` 0.08 |
| 11 | …between March and August → ? | `.` | 0.121 | 3 | `␣` 0.31, `,` 0.29, `.` 0.12, `␣of` 0.05, `␣in` 0.03 |
| 12 | …March and August. → ? | `␣Wells` | 0.000 | 2274 | `␣The` 0.21, `␣In` 0.08, `␣This` 0.04, `␣It` 0.03, `␣However` 0.03 |
| 13 | …and August. Wells → ? | `␣dried` | 0.003 | 33 | `␣were` 0.16, `␣and` 0.10, `,` 0.10, `␣in` 0.08, `␣of` 0.03 |
| 14 | …August. Wells dried → ? | `␣up` | 0.648 | 1 | `␣up` 0.65, `␣out` 0.20, `␣to` 0.02, `␣in` 0.01, `␣and` 0.01 |
| 15 | …. Wells dried up → ? | `␣and` | 0.136 | 2 | `␣in` 0.22, `␣and` 0.14, `,` 0.08, `␣during` 0.07, `␣after` 0.05 |
| 16 | …Wells dried up and → ? | `␣farmers` | 0.009 | 12 | `␣the` 0.17, `␣water` 0.05, `␣a` 0.02, `␣there` 0.02, `␣many` 0.02 |
| 17 | …dried up and farmers → ? | `␣could` | 0.020 | 6 | `␣had` 0.14, `␣were` 0.09, `␣lost` 0.04, `␣struggled` 0.04, `␣began` 0.03 |
| 18 | …up and farmers could → ? | `␣not` | 0.759 | 1 | `␣not` 0.76, `␣no` 0.09, `␣only` 0.03, `␣see` 0.02, `␣barely` 0.02 |
| 19 | …and farmers could not → ? | `␣irrig` | 0.041 | 4 | `␣grow` 0.16, `␣plant` 0.14, `␣get` 0.08, `␣irrig` 0.04, `␣continue` 0.04 |
| 20 | …farmers could not irrig → ? | `ate` | 1.000 | 1 | `ate` 1.00, `ated` 0.00, `at` 0.00, `ating` 0.00, `ates` 0.00 |
| 21 | …could not irrigate → ? | `␣their` | 0.364 | 1 | `␣their` 0.36, `.` 0.11, `␣crops` 0.09, `␣the` 0.06, `,` 0.03 |
| 22 | …not irrigate their → ? | `␣fields` | 0.403 | 1 | `␣fields` 0.40, `␣crops` 0.38, `␣land` 0.07, `␣lands` 0.04, `␣farms` 0.03 |
| 23 | …irrigate their fields → ? | `.` | 0.441 | 1 | `.` 0.44, `,` 0.07, `.\n` 0.06, `␣as` 0.04, `␣for` 0.04 |
| 24 | …ate their fields. → ? | `␣Because` | 0.003 | 50 | `␣The` 0.17, `␣In` 0.06, `␣By` 0.02, `␣A` 0.02, `␣As` 0.02 |
| 25 | …their fields. Because → ? | `␣of` | 0.730 | 1 | `␣of` 0.73, `␣the` 0.10, `␣they` 0.02, `␣there` 0.01, `␣water` 0.01 |
| 26 | …fields. Because of → ? | `␣the` | 0.281 | 2 | `␣this` 0.36, `␣the` 0.28, `␣these` 0.05, `␣drought` 0.04, `␣a` 0.02 |
| 27 | …. Because of the → ? | `␣drought` | 0.143 | 2 | `␣lack` 0.15, `␣drought` 0.14, `␣dry` 0.05, `␣high` 0.03, `␣low` 0.03 |
| 28 | …Because of the drought → ? | `,` | 0.813 | 1 | `,` 0.81, `␣and` 0.04, `␣conditions` 0.04, `␣the` 0.02, `␣in` 0.02 |
| 29 | …of the drought, → ? | `␣the` | 0.184 | 1 | `␣the` 0.18, `␣farmers` 0.07, `␣many` 0.05, `␣some` 0.03, `␣they` 0.02 |
| 30 | …the drought, the → ? | `␣wheat` | 0.006 | 19 | `␣region` 0.05, `␣farmers` 0.03, `␣area` 0.03, `␣water` 0.02, `␣crop` 0.02 |
| 31 | …drought, the wheat → ? | `␣harvest` | 0.136 | 2 | `␣crop` 0.33, `␣harvest` 0.14, `␣crops` 0.05, `␣yield` 0.04, `␣was` 0.04 |
| 32 | …, the wheat harvest → ? | `␣was` | 0.391 | 1 | `␣was` 0.39, `␣in` 0.07, `␣had` 0.04, `␣is` 0.03, `␣failed` 0.02 |
| 33 | …the wheat harvest was → ? | `␣the` | 0.003 | 53 | `␣delayed` 0.13, `␣reduced` 0.09, `␣not` 0.04, `␣low` 0.04, `␣very` 0.03 |
| 34 | …wheat harvest was the → ? | `␣smallest` | 0.032 | 11 | `␣lowest` 0.21, `␣second` 0.10, `␣worst` 0.08, `␣only` 0.08, `␣largest` 0.07 |
| 35 | …harvest was the smallest → ? | `␣in` | 0.415 | 1 | `␣in` 0.41, `␣of` 0.12, `␣on` 0.09, `␣since` 0.06, `␣it` 0.06 |
| 36 | …was the smallest in → ? | `␣forty` | 0.002 | 38 | `␣the` 0.29, `␣` 0.18, `␣more` 0.04, `␣a` 0.04, `␣nearly` 0.04 |
| 37 | …the smallest in forty → ? | `␣years` | 0.648 | 1 | `␣years` 0.65, `-five` 0.14, `-four` 0.05, `-e` 0.03, `-se` 0.03 |
| 38 | …smallest in forty years → ? | `.` | 0.467 | 1 | `.` 0.47, `,` 0.15, `.\n` 0.14, `␣and` 0.06, `␣of` 0.04 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.519 | 1 | `.` 0.52, `!` 0.03, `)` 0.02, `).` 0.01, `?` 0.01 |
| 2 | ? ← . | `␣years` | 0.004 | 5 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣Yes` 0.00, `␣years` 0.00 |
| 3 | ? ← years. | `␣forty` | 0.002 | 64 | `0` 0.06, `␣of` 0.05, `10` 0.04, `20` 0.04, `␣two` 0.03 |
| 4 | ? ← forty years. | `␣in` | 0.023 | 9 | `␣to` 0.13, `␣over` 0.13, `␣than` 0.09, `␣past` 0.08, `␣next` 0.08 |
| 5 | ? ← in forty years. | `␣smallest` | 0.000 | 957 | `␣time` 0.07, `␣seen` 0.02, `␣once` 0.01, `␣been` 0.01, `␣times` 0.01 |
| 6 | ? ← smallest in forty years… | `␣the` | 0.686 | 1 | `␣the` 0.69, `␣its` 0.11, `␣The` 0.08, `␣their` 0.02, `␣second` 0.01 |
| 7 | ? ← the smallest in forty… | `␣was` | 0.183 | 2 | `␣is` 0.20, `␣was` 0.18, `␣be` 0.15, `,` 0.08, `␣and` 0.07 |
| 8 | ? ← was the smallest in… | `␣harvest` | 0.001 | 128 | `␣It` 0.32, `␣it` 0.12, `␣which` 0.04, `␣population` 0.03, `,` 0.02 |
| 9 | ? ← harvest was the smallest… | `␣wheat` | 0.012 | 13 | `␣The` 0.10, `␣the` 0.08, `'s` 0.07, `16` 0.03, `␣salmon` 0.02 |
| 10 | ? ← wheat harvest was the… | `␣the` | 0.090 | 3 | `'s` 0.22, `␣winter` 0.09, `␣the` 0.09, `␣The` 0.07, `␣spring` 0.04 |
| 11 | ? ← the wheat harvest was… | `,` | 0.355 | 1 | `,` 0.35, `␣and` 0.16, `␣that` 0.08, `␣said` 0.04, `␣when` 0.04 |
| 12 | ? ← , the wheat harvest… | `␣drought` | 0.006 | 37 | `␣No` 0.09, `␣year` 0.04, `␣Yes` 0.02, `19` 0.02, `20` 0.02 |
| 13 | ? ← drought, the wheat… | `␣the` | 0.250 | 1 | `␣the` 0.25, `␣severe` 0.08, `␣of` 0.04, `␣a` 0.03, `'s` 0.03 |
| 14 | ? ← the drought, the… | `␣of` | 0.290 | 1 | `␣of` 0.29, `␣to` 0.20, `␣During` 0.13, `␣Despite` 0.11, `␣After` 0.04 |
| 15 | ? ← of the drought,… | `␣Because` | 0.104 | 2 | `␣end` 0.13, `␣Because` 0.10, `␣height` 0.10, `␣result` 0.09, `␣years` 0.08 |
| 16 | ? ← Because of the drought… | `.` | 0.412 | 2 | `:` 0.56, `.` 0.41, `).` 0.01, `)` 0.00, `-` 0.00 |
| 17 | ? ← . Because of the… | `␣fields` | 0.005 | 19 | `␣wheat` 0.04, `␣years` 0.03, `␣harvest` 0.02, `␣drought` 0.02, `␣year` 0.02 |
| 18 | ? ← fields. Because of… | `␣their` | 0.110 | 3 | `␣the` 0.27, `␣wheat` 0.21, `␣their` 0.11, `␣rice` 0.01, `␣in` 0.01 |
| 19 | ? ← their fields. Because… | `ate` | 0.018 | 7 | `␣in` 0.28, `␣to` 0.08, `␣of` 0.07, `␣on` 0.07, `␣from` 0.05 |
| 20 | ? ← ate their fields.… | `␣irrig` | 0.917 | 1 | `␣irrig` 0.92, `␣devast` 0.02, `rig` 0.02, `␣rejuven` 0.01, `␣satur` 0.01 |
| 21 | ? ← irrigate their fields… | `␣not` | 0.021 | 3 | `␣to` 0.79, `␣and` 0.06, `␣not` 0.02, `␣farmers` 0.02, `␣or` 0.01 |
| 22 | ? ← not irrigate their… | `␣could` | 0.298 | 2 | `␣did` 0.60, `␣could` 0.30, `␣do` 0.05, `␣to` 0.02, `␣would` 0.01 |
| 23 | ? ← could not irrigate… | `␣farmers` | 0.385 | 1 | `␣farmers` 0.38, `␣they` 0.21, `␣who` 0.07, `␣Farmers` 0.06, `␣and` 0.05 |
| 24 | ? ← farmers could not irrig… | `␣and` | 0.123 | 2 | `,` 0.15, `␣and` 0.12, `␣that` 0.11, `␣many` 0.08, `␣the` 0.08 |
| 25 | ? ← and farmers could not… | `␣up` | 0.003 | 28 | `,` 0.43, `␣dry` 0.02, `␣drought` 0.02, `␣crops` 0.01, `␣flooded` 0.01 |
| 26 | ? ← up and farmers could… | `␣dried` | 0.468 | 1 | `␣dried` 0.47, `␣dry` 0.23, `␣drying` 0.12, `␣went` 0.02, `ed` 0.01 |
| 27 | ? ← dried up and farmers… | `␣Wells` | 0.000 | 347 | `␣fields` 0.12, `␣had` 0.12, `␣crops` 0.06, `␣rivers` 0.05, `␣supplies` 0.03 |
| 28 | ? ← Wells dried up and… | `.` | 0.854 | 1 | `.` 0.85, `:` 0.06, `␣Indian` 0.01, `␣the` 0.01, `␣Water` 0.01 |
| 29 | ? ← . Wells dried up… | `␣August` | 0.002 | 99 | `␣drought` 0.04, `␣crops` 0.02, `␣fields` 0.02, `␣years` 0.02, `␣wheat` 0.02 |
| 30 | ? ← August. Wells dried… | `␣and` | 0.115 | 3 | `␣in` 0.38, `␣of` 0.12, `␣and` 0.11, `␣early` 0.08, `␣late` 0.07 |
| 31 | ? ← and August. Wells… | `␣March` | 0.003 | 7 | `␣July` 0.87, `,` 0.08, `␣June` 0.03, `␣May` 0.01, `July` 0.01 |
| 32 | ? ← March and August.… | `␣between` | 0.161 | 2 | `␣in` 0.55, `␣between` 0.16, `␣of` 0.08, `␣late` 0.05, `␣during` 0.04 |
| 33 | ? ← between March and August… | `␣rain` | 0.021 | 7 | `␣drought` 0.07, `␣occurred` 0.06, `␣rainfall` 0.03, `␣dry` 0.03, `␣fell` 0.02 |
| 34 | ? ← rain between March and… | `␣no` | 0.128 | 2 | `␣of` 0.43, `␣no` 0.13, `␣little` 0.08, `␣heavy` 0.07, `␣without` 0.04 |
| 35 | ? ← no rain between March… | `␣almost` | 0.172 | 3 | `␣was` 0.22, `␣or` 0.18, `␣almost` 0.17, `␣virtually` 0.09, `␣to` 0.07 |
| 36 | ? ← almost no rain between… | `␣received` | 0.034 | 7 | `␣was` 0.39, `␣with` 0.14, `␣and` 0.09, `␣had` 0.08, `␣of` 0.06 |
| 37 | ? ← received almost no rain… | `␣region` | 0.035 | 5 | `␣had` 0.06, `,` 0.05, `␣area` 0.04, `␣we` 0.04, `␣region` 0.03 |
| 38 | ? ← region received almost no… | `The` | 0.034 | 3 | `␣the` 0.42, `␣The` 0.28, `The` 0.03, `␣This` 0.02, `␣this` 0.02 |

---

## 4. late_train

*Category: temporal*

> **Beginning:** Sarah woke up late because her alarm did not go off.  
> **Middle:** She skipped breakfast and ran to the station, but the doors closed just as she reached the platform.  
> **Ending:** She finally arrived at the office an hour after the meeting had started.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | about it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it, I don't want to talk about it," she said. ↵  ↵ | She finally arrived at the office an hour after the meeting had started. |
| sample | then she is the best group of people to meet and talk to when she is here," she said. ↵  ↵ They all have to work together, even if they are working by themselves. They have to do the work, she said. She said it is important to pay attention to employees and let them know exactly what to do. ↵  ↵ "They have to go and do the work, because those are the things we are there for them to do while they are working with me," she said. ↵  ↵ | She finally arrived at the office an hour after the meeting had started. |
| sample | the office. ↵ He was staring at him. “Oh, it’s too late to get home.” ↵ He was staring at her. She frowned and frowned. ↵ She was trying to get to the office when she heard it keep going off. ↵ She frowned and said, “Oh, it’s too late to get home.” ↵ She went back and turned the lights off. But it still wouldn’t come back on and she was out of room to work in. ↵ | She finally arrived at the office an hour after the meeting had started. |
| sample | for it. “Thank you, things are going well, and this system is working,” she said. ↵ When she asked whether she was in the office by the next day, her manager told her that she was listening to them. ↵ “It's all going well, I'm excited about work, and I want to be here for me,” she said. ↵ “If you can see me, if you can see me now, I'll be able to fit in,” she said. ↵ | She finally arrived at the office an hour after the meeting had started. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | Sarah woke up late because her alarm did not go off. | She was in the middle of the night, and she was not sure what to do. She was worried that she would be late for her class, and she was not sure what to do. She was not sure what to do, and she was not sure what to do. She was not sure what to do, and she was not sure what to do. She was not sure what to do, and she was not sure what to do. She was not sure what to |
| sample | Sarah woke up late because her alarm did not go off. | She was 23 and had no time to find her way to the park or to school. When Sarah walked to her car, the engine sounded like it would start on her car. Suddenly, she turned the key to the start position in the parking lot. She stopped and turned the key to park the car. Then, she turned the key to start the car again. She found herself with no time to go to school, to work, or to take care of her sick |
| sample | Sarah woke up late because her alarm did not go off. | Her friends were all over the place crying, she still had a 5-hour delay. She had lost the ability to hear. Her parents would tell her to go to the doctor because she was crying. The doctor told Sarah that she could not leave because she was in a car. Sarah woke up late because her heart rate was too much and she was not feeling well. Sarah woke up late because she could not hear her friends. Sarah woke up late because she |
| sample | Sarah woke up late because her alarm did not go off. | Her alarm bell did not ring, and she would not wake to see what was going on. She was not alone, and she was not alone. Sarah's alarm went off, but she didn't wake up to see what was going on. Sarah woke up late because her alarm did not go off. Her alarm bell did not ring, and she would not wake to see what was going on. Sarah, her sister, and Sarah's husband were all asleep. They were |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.934 | 43% |
| Backward | previous-token (right context) | 1.004 | 39% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `Sar` | 0.000 | 1145 | `The` 0.06, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | Sar → ? | `ah` | 0.622 | 1 | `ah` 0.62, `co` 0.11, `rac` 0.03, `aw` 0.02, `us` 0.01 |
| 3 | Sarah → ? | `␣w` | 0.000 | 781 | `:` 0.08, `'s` 0.08, `,` 0.06, `␣is` 0.02, `␣and` 0.02 |
| 4 | Sarah w → ? | `oke` | 0.234 | 2 | `akes` 0.25, `oke` 0.23, `aved` 0.02, `ink` 0.02, `ilson` 0.02 |
| 5 | Sarah woke → ? | `␣up` | 0.967 | 1 | `␣up` 0.97, `␣her` 0.01, `␣me` 0.00, `␣early` 0.00, `␣from` 0.00 |
| 6 | …ah woke up → ? | `␣late` | 0.018 | 12 | `␣early` 0.14, `␣in` 0.11, `␣one` 0.11, `␣at` 0.09, `␣this` 0.05 |
| 7 | …woke up late → ? | `␣because` | 0.006 | 19 | `␣at` 0.18, `␣one` 0.14, `,` 0.09, `␣and` 0.08, `␣in` 0.08 |
| 8 | …oke up late because → ? | `␣her` | 0.160 | 3 | `␣she` 0.47, `␣of` 0.22, `␣her` 0.16, `␣the` 0.03, `␣I` 0.01 |
| 9 | …up late because her → ? | `␣alarm` | 0.011 | 17 | `␣husband` 0.06, `␣phone` 0.02, `␣mother` 0.02, `␣daughter` 0.02, `␣parents` 0.02 |
| 10 | …late because her alarm → ? | `␣did` | 0.001 | 15 | `␣clock` 0.80, `␣went` 0.06, `␣had` 0.04, `␣clocks` 0.01, `␣was` 0.01 |
| 11 | …because her alarm did → ? | `␣not` | 0.976 | 1 | `␣not` 0.98, `␣go` 0.01, `␣nothing` 0.00, `␣something` 0.00, `␣ring` 0.00 |
| 12 | …her alarm did not → ? | `␣go` | 0.511 | 1 | `␣go` 0.51, `␣ring` 0.12, `␣sound` 0.12, `␣wake` 0.06, `␣work` 0.04 |
| 13 | …alarm did not go → ? | `␣off` | 0.974 | 1 | `␣off` 0.97, `␣through` 0.00, `␣to` 0.00, `␣out` 0.00, `␣down` 0.00 |
| 14 | …did not go off → ? | `.` | 0.322 | 1 | `.` 0.32, `␣at` 0.12, `,` 0.12, `␣when` 0.05, `␣and` 0.05 |
| 15 | …not go off. → ? | `␣She` | 0.388 | 1 | `␣She` 0.39, `␣Her` 0.09, `␣The` 0.05, `␣Sarah` 0.03, `␣It` 0.03 |
| 16 | …go off. She → ? | `␣sk` | 0.000 | 223 | `␣was` 0.20, `␣had` 0.13, `␣went` 0.04, `␣didn` 0.03, `␣w` 0.03 |
| 17 | …off. She sk → ? | `ipped` | 0.945 | 1 | `ipped` 0.94, `idd` 0.02, `ied` 0.01, `ips` 0.01, `ir` 0.01 |
| 18 | …. She skipped → ? | `␣breakfast` | 0.205 | 1 | `␣breakfast` 0.21, `␣a` 0.13, `␣class` 0.10, `␣school` 0.09, `␣classes` 0.06 |
| 19 | …She skipped breakfast → ? | `␣and` | 0.294 | 2 | `,` 0.30, `␣and` 0.29, `.` 0.07, `␣at` 0.04, `␣because` 0.03 |
| 20 | …skipped breakfast and → ? | `␣ran` | 0.011 | 17 | `␣went` 0.14, `␣was` 0.07, `␣then` 0.06, `␣lunch` 0.04, `␣had` 0.03 |
| 21 | …ipped breakfast and ran → ? | `␣to` | 0.329 | 1 | `␣to` 0.33, `␣home` 0.16, `␣out` 0.11, `␣into` 0.08, `␣around` 0.04 |
| 22 | …breakfast and ran to → ? | `␣the` | 0.623 | 1 | `␣the` 0.62, `␣her` 0.14, `␣work` 0.06, `␣bed` 0.03, `␣school` 0.03 |
| 23 | …and ran to the → ? | `␣station` | 0.000 | 397 | `␣bathroom` 0.23, `␣kitchen` 0.16, `␣door` 0.07, `␣car` 0.07, `␣front` 0.06 |
| 24 | …ran to the station → ? | `,` | 0.142 | 3 | `.` 0.22, `␣to` 0.21, `,` 0.14, `␣for` 0.05, `␣where` 0.03 |
| 25 | …to the station, → ? | `␣but` | 0.064 | 2 | `␣where` 0.08, `␣but` 0.06, `␣only` 0.06, `␣which` 0.03, `␣her` 0.02 |
| 26 | …the station, but → ? | `␣the` | 0.107 | 1 | `␣the` 0.11, `␣she` 0.08, `␣was` 0.07, `␣her` 0.06, `␣then` 0.06 |
| 27 | …station, but the → ? | `␣doors` | 0.004 | 41 | `␣alarm` 0.15, `␣bus` 0.03, `␣train` 0.03, `␣car` 0.03, `␣door` 0.02 |
| 28 | …, but the doors → ? | `␣closed` | 0.029 | 7 | `␣were` 0.23, `␣did` 0.09, `␣to` 0.05, `␣would` 0.03, `␣remained` 0.03 |
| 29 | …but the doors closed → ? | `␣just` | 0.014 | 13 | `.` 0.25, `␣and` 0.17, `,` 0.08, `␣at` 0.03, `␣when` 0.02 |
| 30 | …the doors closed just → ? | `␣as` | 0.380 | 1 | `␣as` 0.38, `␣before` 0.19, `␣a` 0.09, `␣in` 0.05, `␣then` 0.03 |
| 31 | …doors closed just as → ? | `␣she` | 0.529 | 1 | `␣she` 0.53, `␣the` 0.13, `␣her` 0.08, `␣Sarah` 0.07, `␣they` 0.05 |
| 32 | …closed just as she → ? | `␣reached` | 0.025 | 10 | `␣was` 0.20, `␣got` 0.09, `␣went` 0.07, `␣w` 0.05, `␣walked` 0.04 |
| 33 | …just as she reached → ? | `␣the` | 0.700 | 1 | `␣the` 0.70, `␣her` 0.07, `␣home` 0.05, `␣out` 0.03, `␣for` 0.02 |
| 34 | …as she reached the → ? | `␣platform` | 0.001 | 150 | `␣door` 0.06, `␣bus` 0.05, `␣station` 0.03, `␣bathroom` 0.03, `␣gate` 0.03 |
| 35 | …she reached the platform → ? | `.` | 0.478 | 1 | `.` 0.48, `,` 0.08, `␣where` 0.05, `␣and` 0.04, `␣to` 0.04 |
| 36 | …reached the platform. → ? | `␣She` | 0.243 | 1 | `␣She` 0.24, `␣The` 0.11, `␣Her` 0.07, `␣Sarah` 0.05, `␣As` 0.04 |
| 37 | …the platform. She → ? | `␣finally` | 0.002 | 77 | `␣was` 0.14, `␣had` 0.05, `␣could` 0.02, `␣ran` 0.02, `␣turned` 0.02 |
| 38 | …platform. She finally → ? | `␣arrived` | 0.020 | 11 | `␣got` 0.19, `␣found` 0.04, `␣managed` 0.03, `␣reached` 0.03, `␣made` 0.03 |
| 39 | …. She finally arrived → ? | `␣at` | 0.394 | 1 | `␣at` 0.39, `,` 0.11, `␣to` 0.07, `␣and` 0.07, `.` 0.04 |
| 40 | …She finally arrived at → ? | `␣the` | 0.783 | 1 | `␣the` 0.78, `␣her` 0.04, `␣` 0.04, `␣a` 0.03, `␣work` 0.00 |
| 41 | …finally arrived at the → ? | `␣office` | 0.011 | 12 | `␣station` 0.12, `␣door` 0.04, `␣platform` 0.04, `␣gate` 0.03, `␣train` 0.03 |
| 42 | …arrived at the office → ? | `␣an` | 0.000 | 95 | `,` 0.26, `␣and` 0.15, `.` 0.07, `␣to` 0.06, `␣where` 0.05 |
| 43 | …at the office an → ? | `␣hour` | 0.970 | 1 | `␣hour` 0.97, `␣alarm` 0.00, `␣early` 0.00, `␣hours` 0.00, `␣an` 0.00 |
| 44 | …the office an hour → ? | `␣after` | 0.058 | 2 | `␣later` 0.78, `␣after` 0.06, `␣and` 0.05, `␣late` 0.03, `␣before` 0.02 |
| 45 | …office an hour after → ? | `␣the` | 0.077 | 2 | `␣` 0.09, `␣the` 0.08, `␣sunrise` 0.07, `␣her` 0.06, `␣midnight` 0.06 |
| 46 | …an hour after the → ? | `␣meeting` | 0.005 | 29 | `␣alarm` 0.21, `␣train` 0.04, `␣sun` 0.03, `␣` 0.02, `␣first` 0.02 |
| 47 | …hour after the meeting → ? | `␣had` | 0.064 | 4 | `.` 0.24, `,` 0.23, `␣and` 0.07, `␣had` 0.06, `␣was` 0.05 |
| 48 | …after the meeting had → ? | `␣started` | 0.208 | 2 | `␣begun` 0.35, `␣started` 0.21, `␣ended` 0.11, `␣been` 0.08, `␣finished` 0.03 |
| 49 | …the meeting had started → ? | `.` | 0.403 | 1 | `.` 0.40, `,` 0.32, `␣and` 0.08, `.\n` 0.06, `␣to` 0.02 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.519 | 1 | `.` 0.52, `!` 0.03, `)` 0.02, `).` 0.01, `?` 0.01 |
| 2 | ? ← . | `␣started` | 0.000 | 726 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣Yes` 0.00, `␣years` 0.00 |
| 3 | ? ← started. | `␣had` | 0.003 | 32 | `␣get` 0.40, `␣you` 0.15, `␣getting` 0.06, `␣has` 0.02, `␣be` 0.02 |
| 4 | ? ← had started. | `␣meeting` | 0.001 | 50 | `␣they` 0.13, `␣it` 0.10, `␣he` 0.07, `␣I` 0.04, `␣she` 0.03 |
| 5 | ? ← meeting had started. | `␣the` | 0.574 | 1 | `␣the` 0.57, `␣The` 0.04, `␣a` 0.04, `␣their` 0.02, `␣first` 0.02 |
| 6 | ? ← the meeting had started… | `␣after` | 0.354 | 1 | `␣after` 0.35, `␣before` 0.17, `␣that` 0.07, `␣once` 0.06, `␣since` 0.03 |
| 7 | ? ← after the meeting had… | `␣hour` | 0.015 | 14 | `␣minutes` 0.06, `␣until` 0.06, `␣long` 0.05, `␣hours` 0.05, `␣days` 0.05 |
| 8 | ? ← hour after the meeting… | `␣an` | 0.652 | 1 | `␣an` 0.65, `␣one` 0.14, `␣half` 0.06, `␣An` 0.04, `1` 0.04 |
| 9 | ? ← an hour after the… | `␣office` | 0.001 | 77 | `␣half` 0.17, `␣about` 0.11, `␣than` 0.10, `␣About` 0.05, `␣within` 0.04 |
| 10 | ? ← office an hour after… | `␣the` | 0.455 | 1 | `␣the` 0.46, `'s` 0.11, `␣my` 0.03, `␣his` 0.03, `␣our` 0.02 |
| 11 | ? ← the office an hour… | `␣at` | 0.116 | 4 | `␣to` 0.23, `␣left` 0.17, `␣in` 0.15, `␣at` 0.12, `␣into` 0.10 |
| 12 | ? ← at the office an… | `␣arrived` | 0.155 | 1 | `␣arrived` 0.15, `␣arrive` 0.07, `␣be` 0.05, `␣up` 0.05, `␣was` 0.04 |
| 13 | ? ← arrived at the office… | `␣finally` | 0.003 | 33 | `␣I` 0.10, `␣He` 0.07, `␣and` 0.07, `␣they` 0.06, `␣She` 0.05 |
| 14 | ? ← finally arrived at the… | `␣She` | 0.046 | 5 | `␣and` 0.13, `␣I` 0.11, `␣He` 0.07, `␣he` 0.06, `␣they` 0.05 |
| 15 | ? ← She finally arrived at… | `.` | 0.453 | 2 | `:` 0.51, `.` 0.45, `."` 0.01, `!` 0.01, `).` 0.00 |
| 16 | ? ← . She finally arrived… | `␣platform` | 0.000 | 3920 | `␣meeting` 0.04, `␣her` 0.02, `␣time` 0.01, `␣office` 0.01, `␣minutes` 0.01 |
| 17 | ? ← platform. She finally… | `␣the` | 0.254 | 1 | `␣the` 0.25, `␣online` 0.06, `␣her` 0.05, `␣media` 0.04, `␣a` 0.03 |
| 18 | ? ← the platform. She… | `␣reached` | 0.002 | 34 | `␣on` 0.41, `␣to` 0.09, `␣of` 0.05, `␣off` 0.05, `␣from` 0.04 |
| 19 | ? ← reached the platform.… | `␣she` | 0.440 | 1 | `␣she` 0.44, `␣never` 0.08, `␣had` 0.07, `␣finally` 0.05, `␣and` 0.04 |
| 20 | ? ← she reached the platform… | `␣as` | 0.092 | 4 | `␣before` 0.25, `␣until` 0.21, `␣when` 0.20, `␣as` 0.09, `␣time` 0.05 |
| 21 | ? ← as she reached the… | `␣just` | 0.008 | 5 | `␣soon` 0.39, `␣her` 0.03, `"` 0.01, `,` 0.01, `ed` 0.01 |
| 22 | ? ← just as she reached… | `␣closed` | 0.001 | 110 | `,` 0.09, `␣her` 0.04, `␣meeting` 0.03, `␣office` 0.03, `␣up` 0.01 |
| 23 | ? ← closed just as she… | `␣doors` | 0.040 | 5 | `␣eyes` 0.21, `␣door` 0.10, `␣was` 0.06, `␣had` 0.04, `␣doors` 0.04 |
| 24 | ? ← doors closed just as… | `␣the` | 0.370 | 1 | `␣the` 0.37, `␣The` 0.14, `␣office` 0.11, `'s` 0.02, `The` 0.02 |
| 25 | ? ← the doors closed just… | `␣but` | 0.046 | 8 | `,` 0.18, `␣and` 0.15, `␣as` 0.08, `␣that` 0.06, `␣of` 0.06 |
| 26 | ? ← but the doors closed… | `,` | 0.789 | 1 | `,` 0.79, `␣meeting` 0.02, `␣office` 0.01, `␣room` 0.00, `␣her` 0.00 |
| 27 | ? ← , but the doors… | `␣station` | 0.001 | 99 | `␣meeting` 0.10, `␣office` 0.04, `␣her` 0.02, `␣room` 0.02, `␣door` 0.01 |
| 28 | ? ← station, but the… | `␣the` | 0.315 | 1 | `␣the` 0.32, `␣radio` 0.09, `␣train` 0.06, `␣police` 0.05, `␣bus` 0.01 |
| 29 | ? ← the station, but… | `␣to` | 0.242 | 2 | `␣at` 0.30, `␣to` 0.24, `␣of` 0.05, `␣reach` 0.04, `␣from` 0.03 |
| 30 | ? ← to the station,… | `␣ran` | 0.002 | 65 | `␣back` 0.10, `␣get` 0.09, `␣her` 0.06, `␣way` 0.05, `␣up` 0.03 |
| 31 | ? ← ran to the station… | `␣and` | 0.206 | 1 | `␣and` 0.21, `␣She` 0.19, `␣she` 0.09, `She` 0.03, `␣then` 0.03 |
| 32 | ? ← and ran to the… | `␣breakfast` | 0.001 | 269 | `␣up` 0.05, `,` 0.05, `␣door` 0.03, `␣car` 0.03, `ed` 0.02 |
| 33 | ? ← breakfast and ran to… | `ipped` | 0.011 | 13 | `␣her` 0.31, `␣for` 0.16, `␣ate` 0.09, `␣had` 0.06, `␣made` 0.04 |
| 34 | ? ← ipped breakfast and ran… | `␣sk` | 0.987 | 1 | `␣sk` 0.99, `␣s` 0.01, `␣Sk` 0.00, `␣t` 0.00, `-l` 0.00 |
| 35 | ? ← skipped breakfast and… | `␣She` | 0.309 | 1 | `␣She` 0.31, `␣she` 0.08, `,` 0.07, `She` 0.06, `␣had` 0.05 |
| 36 | ? ← She skipped breakfast… | `.` | 0.912 | 1 | `.` 0.91, `."` 0.03, `:` 0.02, `!` 0.01, `!"` 0.00 |
| 37 | ? ← . She skipped… | `␣off` | 0.005 | 20 | `␣station` 0.05, `␣meeting` 0.02, `␣office` 0.02, `␣breakfast` 0.02, `␣door` 0.01 |
| 38 | ? ← off. She sk… | `␣go` | 0.015 | 14 | `␣went` 0.07, `␣took` 0.07, `␣was` 0.04, `␣it` 0.04, `␣take` 0.04 |
| 39 | ? ← go off. She… | `␣not` | 0.034 | 5 | `␣to` 0.64, `'t` 0.07, `␣would` 0.04, `␣alarm` 0.04, `␣not` 0.03 |
| 40 | ? ← not go off.… | `␣did` | 0.739 | 1 | `␣did` 0.74, `␣would` 0.21, `␣could` 0.01, `␣to` 0.01, `␣and` 0.00 |
| 41 | ? ← did not go off… | `␣alarm` | 0.311 | 1 | `␣alarm` 0.31, `␣lights` 0.06, `␣light` 0.04, `␣radio` 0.04, `␣alarms` 0.03 |
| 42 | ? ← alarm did not go… | `␣her` | 0.100 | 3 | `␣the` 0.49, `␣The` 0.11, `␣her` 0.10, `␣fire` 0.03, `␣smoke` 0.03 |
| 43 | ? ← her alarm did not… | `␣because` | 0.021 | 6 | `␣but` 0.28, `,` 0.22, `␣and` 0.19, `␣that` 0.07, `␣why` 0.03 |
| 44 | ? ← because her alarm did… | `␣late` | 0.019 | 6 | `,` 0.09, `␣station` 0.04, `␣morning` 0.03, `␣alarm` 0.03, `␣office` 0.02 |
| 45 | ? ← late because her alarm… | `␣up` | 0.047 | 5 | `␣was` 0.24, `␣minutes` 0.11, `␣running` 0.10, `␣arrived` 0.06, `␣up` 0.05 |
| 46 | ? ← up late because her… | `oke` | 0.172 | 2 | `␣stayed` 0.29, `oke` 0.17, `␣stay` 0.12, `␣showed` 0.08, `␣got` 0.06 |
| 47 | ? ← oke up late because… | `␣w` | 0.987 | 1 | `␣w` 0.99, `␣aw` 0.00, `␣W` 0.00, `W` 0.00, `ken` 0.00 |
| 48 | ? ← woke up late… | `ah` | 0.001 | 51 | `␣she` 0.19, `␣She` 0.13, `␣and` 0.08, `,` 0.04, `␣but` 0.03 |
| 49 | ? ← ah woke up… | `Sar` | 0.407 | 1 | `Sar` 0.41, `bor` 0.09, `␣Le` 0.06, `Le` 0.03, `j` 0.03 |

---

## 5. bread_recipe

*Category: temporal*

> **Beginning:** First, mix the flour, yeast, salt and warm water in a large bowl.  
> **Middle:** Knead the dough for ten minutes, then leave it to rise for an hour until it has doubled in size.  
> **Ending:** Finally, bake the loaf at 220 degrees for thirty minutes until it is golden brown.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | dough and place it on top of the mixture. Then, spread the mixture evenly over the top of the dough. ↵  ↵ First, make a hole in the center of the dough and place it on top of the mixture. Then, make a hole in the center of the dough and place it on top of the mixture. ↵  ↵ Next, make a hole in the center of the dough and place it on top of the mixture. Then, spread the mixture evenly over the top of the dough. ↵  ↵ | Finally, bake the loaf at 220 degrees for thirty minutes until it is golden brown. |
| sample | it, mix the flour together, pour it into the bowl, and distribute the ingredients evenly in the pan. ↵  ↵ Once all of the ingredients are prepared, the next step is to bake them at 220 degrees for thirty minutes. ↵  ↵ Then, get a large piece of dough to put in the loaf. ↵  ↵ In a bowl, add olive oil to the mixture, and rub it all over the top of the bread with the same fat that you use to cover the rest of the dough. ↵  ↵ | Finally, bake the loaf at 220 degrees for thirty minutes until it is golden brown. |
| sample | and the soaking time has elapsed, take the loaf out of the water and let it soak for two hours, or at least overnight. Once it has soaked, remove it and pat it dry. ↵  ↵ Heat the oven to 180 degrees. ↵ Line a baking sheet with parchment paper. ↵ Spoon a portion of the almond mixture over the almond mixture to one side of the leaf square, and adhere it to the parchment paper. Fold around the leaf and place it seam side down. ↵ | Finally, bake the loaf at 220 degrees for thirty minutes until it is golden brown. |
| sample | of flour and cut it into a square shape. ↵ Take a large bowl, take a spoonful of flour, hold it in the palm of your hand, bring it to the dough, push it to the top edge of the dough, fold it over ⅓ of the way up, fold it into the dough, press it to the bottom of the loaf pan, and press it into the dough at the base of the pan, pushing it back down in the dough. ↵ | Finally, bake the loaf at 220 degrees for thirty minutes until it is golden brown. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | First, mix the flour, yeast, salt and warm water in a large bowl. | Add the oil and stir until the mixture is well combined. Add the yeast mixture and stir until it is dissolved. Add the sugar and stir until the sugar is dissolved. Add the flour mixture and stir until the flour is well combined. Add the water and stir until the water is absorbed. Add the salt and stir until the salt is dissolved. Add the yeast mixture and stir until the yeast is dissolved. Add the flour mixture and stir until the flour is well combined. Add the |
| sample | First, mix the flour, yeast, salt and warm water in a large bowl. | Add the egg and mix well. ↵  ↵ Gradually add the warm water to the flour until it becomes a thick paste, then add the yeast. Stir it for a few minutes, then add the water. ↵  ↵ Next, add the milk and knead the dough until it becomes smooth and elastic. Cover the bowl with a clean cloth and let it rest for a few minutes. ↵  ↵ When the dough is ready, knead it for a few minutes, then divide it into 8 equal parts |
| sample | First, mix the flour, yeast, salt and warm water in a large bowl. | Then add the oil and stir well. ↵ Add 1/4 cup of the yeast mix and 1/4 cup of the flour to the warm water. Mix well. ↵ Add the remaining 1/4 cup of yeast mix, warm water and oil to the bowl. Stir until the yeast mix is dissolved and the flour is well combined, then start adding the salt and sugar to the yeast mix. Stir until the yeast mix is well combined and the salt and sugar are added |
| sample | First, mix the flour, yeast, salt and warm water in a large bowl. | Gradually add the oil to the bowl and mix all the ingredients. ↵ Cover the bowl with plastic wrap and let it rest in the refrigerator for at least 2 hours. ↵ When the dough has risen, you can knead it by hand by rolling it up with your hands. ↵ If the dough is too wet, add flour and a little warm water and knead it again until it becomes soft. ↵ If the dough is too dry, add more water and knead it until it becomes elastic |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.623 | 63% |
| Backward | previous-token (right context) | 0.617 | 55% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `First` | 0.001 | 123 | `The` 0.06, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | First → ? | `,` | 0.256 | 1 | `,` 0.26, `␣of` 0.09, `␣Aid` 0.04, `␣off` 0.04, `␣and` 0.01 |
| 3 | First, → ? | `␣mix` | 0.000 | 355 | `␣the` 0.10, `␣let` 0.07, `␣you` 0.07, `␣I` 0.06, `␣we` 0.06 |
| 4 | First, mix → ? | `␣the` | 0.378 | 1 | `␣the` 0.38, `␣` 0.08, `␣your` 0.06, `␣all` 0.05, `␣up` 0.05 |
| 5 | First, mix the → ? | `␣flour` | 0.049 | 1 | `␣flour` 0.05, `␣water` 0.03, `␣ingredients` 0.03, `␣eggs` 0.02, `␣rice` 0.02 |
| 6 | …, mix the flour → ? | `,` | 0.356 | 1 | `,` 0.36, `␣and` 0.32, `␣with` 0.26, `␣into` 0.02, `␣in` 0.01 |
| 7 | …mix the flour, → ? | `␣yeast` | 0.039 | 4 | `␣baking` 0.28, `␣sugar` 0.17, `␣salt` 0.16, `␣yeast` 0.04, `␣water` 0.04 |
| 8 | …the flour, yeast → ? | `,` | 0.866 | 1 | `,` 0.87, `␣and` 0.12, `␣(` 0.00, `␣mixture` 0.00, `␣extract` 0.00 |
| 9 | …flour, yeast, → ? | `␣salt` | 0.179 | 3 | `␣and` 0.38, `␣sugar` 0.20, `␣salt` 0.18, `␣water` 0.06, `␣baking` 0.05 |
| 10 | …, yeast, salt → ? | `␣and` | 0.102 | 2 | `,` 0.89, `␣and` 0.10, `␣(` 0.00, `␣in` 0.00, `␣&` 0.00 |
| 11 | …yeast, salt and → ? | `␣warm` | 0.047 | 4 | `␣sugar` 0.43, `␣water` 0.22, `␣baking` 0.06, `␣warm` 0.05, `␣oil` 0.04 |
| 12 | …, salt and warm → ? | `␣water` | 0.950 | 1 | `␣water` 0.95, `␣milk` 0.03, `␣warm` 0.00, `water` 0.00, `␣tap` 0.00 |
| 13 | …salt and warm water → ? | `␣in` | 0.470 | 1 | `␣in` 0.47, `␣together` 0.20, `␣into` 0.07, `.` 0.07, `␣until` 0.06 |
| 14 | …and warm water in → ? | `␣a` | 0.955 | 1 | `␣a` 0.96, `␣the` 0.02, `␣your` 0.01, `␣an` 0.00, `␣small` 0.00 |
| 15 | …warm water in a → ? | `␣large` | 0.223 | 2 | `␣bowl` 0.44, `␣large` 0.22, `␣small` 0.11, `␣medium` 0.04, `␣mixing` 0.03 |
| 16 | …water in a large → ? | `␣bowl` | 0.741 | 1 | `␣bowl` 0.74, `␣mixing` 0.21, `␣measuring` 0.01, `,` 0.00, `␣pot` 0.00 |
| 17 | …in a large bowl → ? | `.` | 0.645 | 1 | `.` 0.65, `␣and` 0.09, `␣until` 0.07, `,` 0.05, `.\n` 0.05 |
| 18 | …a large bowl. → ? | `␣K` | 0.027 | 8 | `␣Add` 0.26, `␣Gradually` 0.07, `␣Then` 0.07, `␣Stir` 0.05, `␣Cover` 0.04 |
| 19 | …large bowl. K → ? | `ne` | 0.990 | 1 | `ne` 0.99, `iss` 0.00, `osher` 0.00, `IT` 0.00, `ald` 0.00 |
| 20 | …bowl. Kne → ? | `ad` | 0.997 | 1 | `ad` 1.00, `ading` 0.00, `at` 0.00, `aded` 0.00, `ch` 0.00 |
| 21 | …. Knead → ? | `␣the` | 0.646 | 1 | `␣the` 0.65, `␣until` 0.08, `␣for` 0.07, `␣in` 0.05, `␣it` 0.02 |
| 22 | …Knead the → ? | `␣dough` | 0.808 | 1 | `␣dough` 0.81, `␣mixture` 0.09, `␣yeast` 0.02, `␣flour` 0.02, `␣ingredients` 0.02 |
| 23 | …nead the dough → ? | `␣for` | 0.410 | 1 | `␣for` 0.41, `␣until` 0.15, `␣on` 0.12, `␣with` 0.06, `,` 0.03 |
| 24 | …ad the dough for → ? | `␣ten` | 0.003 | 12 | `␣` 0.38, `␣about` 0.34, `␣a` 0.17, `␣at` 0.03, `␣several` 0.01 |
| 25 | …the dough for ten → ? | `␣minutes` | 0.871 | 1 | `␣minutes` 0.87, `␣to` 0.09, `␣seconds` 0.03, `␣or` 0.01, `\n` 0.00 |
| 26 | …dough for ten minutes → ? | `,` | 0.434 | 1 | `,` 0.43, `␣until` 0.18, `.` 0.10, `␣or` 0.07, `␣on` 0.05 |
| 27 | …for ten minutes, → ? | `␣then` | 0.379 | 1 | `␣then` 0.38, `␣or` 0.14, `␣until` 0.13, `␣adding` 0.05, `␣and` 0.03 |
| 28 | …ten minutes, then → ? | `␣leave` | 0.014 | 13 | `␣divide` 0.13, `␣cover` 0.12, `␣add` 0.10, `␣roll` 0.07, `␣kne` 0.06 |
| 29 | …minutes, then leave → ? | `␣it` | 0.716 | 1 | `␣it` 0.72, `␣to` 0.16, `␣for` 0.04, `␣the` 0.02, `␣in` 0.02 |
| 30 | …, then leave it → ? | `␣to` | 0.520 | 1 | `␣to` 0.52, `␣in` 0.23, `␣for` 0.10, `␣on` 0.05, `␣aside` 0.03 |
| 31 | …then leave it to → ? | `␣rise` | 0.496 | 1 | `␣rise` 0.50, `␣rest` 0.41, `␣sit` 0.02, `␣stand` 0.02, `␣proof` 0.02 |
| 32 | …leave it to rise → ? | `␣for` | 0.395 | 1 | `␣for` 0.40, `␣in` 0.29, `␣until` 0.08, `␣again` 0.04, `␣a` 0.02 |
| 33 | …it to rise for → ? | `␣an` | 0.241 | 2 | `␣another` 0.38, `␣an` 0.24, `␣` 0.10, `␣a` 0.06, `␣about` 0.06 |
| 34 | …to rise for an → ? | `␣hour` | 0.590 | 1 | `␣hour` 0.59, `␣additional` 0.40, `␣extra` 0.01, `␣further` 0.00, `␣even` 0.00 |
| 35 | …rise for an hour → ? | `␣until` | 0.026 | 9 | `.` 0.38, `␣or` 0.14, `.\n` 0.11, `,` 0.08, `␣before` 0.07 |
| 36 | …for an hour until → ? | `␣it` | 0.515 | 1 | `␣it` 0.51, `␣doubled` 0.27, `␣the` 0.10, `␣a` 0.02, `␣double` 0.02 |
| 37 | …an hour until it → ? | `␣has` | 0.122 | 4 | `␣doubles` 0.20, `␣is` 0.19, `␣reaches` 0.13, `␣has` 0.12, `␣becomes` 0.10 |
| 38 | …hour until it has → ? | `␣doubled` | 0.773 | 1 | `␣doubled` 0.77, `␣risen` 0.10, `␣a` 0.02, `␣increased` 0.01, `␣become` 0.01 |
| 39 | …until it has doubled → ? | `␣in` | 0.940 | 1 | `␣in` 0.94, `.` 0.02, `.\n` 0.01, `,` 0.01, `␣its` 0.00 |
| 40 | …it has doubled in → ? | `␣size` | 0.845 | 1 | `␣size` 0.84, `␣volume` 0.11, `␣bulk` 0.03, `␣weight` 0.00, `␣mass` 0.00 |
| 41 | …has doubled in size → ? | `.` | 0.540 | 1 | `.` 0.54, `.\n` 0.20, `,` 0.09, `.\n\n` 0.05, `␣and` 0.05 |
| 42 | …doubled in size. → ? | `␣Finally` | 0.000 | 163 | `␣Cover` 0.09, `␣K` 0.06, `␣Divide` 0.06, `␣(` 0.05, `␣The` 0.04 |
| 43 | …in size. Finally → ? | `,` | 0.975 | 1 | `,` 0.98, `␣add` 0.00, `␣divide` 0.00, `␣roll` 0.00, `␣kne` 0.00 |
| 44 | …size. Finally, → ? | `␣bake` | 0.007 | 25 | `␣kne` 0.13, `␣divide` 0.12, `␣roll` 0.09, `␣shape` 0.08, `␣add` 0.04 |
| 45 | …. Finally, bake → ? | `␣the` | 0.619 | 1 | `␣the` 0.62, `␣it` 0.23, `␣for` 0.07, `␣in` 0.03, `␣your` 0.02 |
| 46 | …Finally, bake the → ? | `␣loaf` | 0.017 | 5 | `␣dough` 0.39, `␣bread` 0.31, `␣cookies` 0.05, `␣cake` 0.02, `␣loaf` 0.02 |
| 47 | …, bake the loaf → ? | `␣at` | 0.095 | 3 | `␣for` 0.43, `␣in` 0.36, `␣at` 0.10, `␣until` 0.04, `␣of` 0.02 |
| 48 | …bake the loaf at → ? | `␣` | 0.909 | 1 | `␣` 0.91, `␣a` 0.05, `␣the` 0.02, `␣about` 0.01, `␣least` 0.00 |
| 49 | …the loaf at → ? | `22` | 0.003 | 17 | `35` 0.52, `37` 0.12, `40` 0.11, `32` 0.06, `18` 0.04 |
| 50 | …loaf at 22 → ? | `0` | 0.304 | 2 | `5` 0.69, `0` 0.30, `3` 0.00, `50` 0.00, `␣` 0.00 |
| 51 | …at 220 → ? | `␣degrees` | 0.479 | 1 | `␣degrees` 0.48, `°F` 0.17, `°C` 0.08, `F` 0.06, `°` 0.03 |
| 52 | …220 degrees → ? | `␣for` | 0.441 | 1 | `␣for` 0.44, `␣Fahrenheit` 0.30, `␣F` 0.19, `␣Celsius` 0.02, `␣until` 0.02 |
| 53 | …220 degrees for → ? | `␣thirty` | 0.012 | 8 | `␣` 0.66, `␣about` 0.14, `␣an` 0.04, `␣approximately` 0.02, `␣one` 0.02 |
| 54 | …0 degrees for thirty → ? | `␣minutes` | 0.906 | 1 | `␣minutes` 0.91, `-five` 0.05, `␣to` 0.02, `␣(` 0.00, `-s` 0.00 |
| 55 | …degrees for thirty minutes → ? | `␣until` | 0.043 | 6 | `.\n` 0.24, `.` 0.20, `,` 0.20, `␣or` 0.09, `.\n\n` 0.07 |
| 56 | …for thirty minutes until → ? | `␣it` | 0.327 | 1 | `␣the` 0.33, `␣it` 0.33, `␣a` 0.15, `␣golden` 0.11, `␣set` 0.01 |
| 57 | …thirty minutes until it → ? | `␣is` | 0.509 | 1 | `␣is` 0.51, `␣has` 0.13, `␣reaches` 0.09, `␣comes` 0.05, `'s` 0.05 |
| 58 | …minutes until it is → ? | `␣golden` | 0.358 | 1 | `␣golden` 0.36, `␣a` 0.13, `␣light` 0.08, `␣set` 0.05, `␣lightly` 0.05 |
| 59 | …until it is golden → ? | `␣brown` | 0.778 | 1 | `␣brown` 0.78, `␣and` 0.13, `.\n` 0.03, `.` 0.01, `,` 0.01 |
| 60 | …it is golden brown → ? | `.` | 0.139 | 3 | `␣and` 0.34, `.\n` 0.30, `.` 0.14, `.\n\n` 0.08, `␣on` 0.06 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.519 | 1 | `.` 0.52, `!` 0.03, `)` 0.02, `).` 0.01, `?` 0.01 |
| 2 | ? ← . | `␣brown` | 0.000 | 1856 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣Yes` 0.00, `␣years` 0.00 |
| 3 | ? ← brown. | `␣golden` | 0.062 | 6 | `␣or` 0.12, `␣and` 0.10, `␣turn` 0.07, `␣to` 0.07, `␣dark` 0.06 |
| 4 | ? ← golden brown. | `␣is` | 0.125 | 2 | `␣until` 0.31, `␣is` 0.13, `␣turn` 0.09, `␣and` 0.08, `␣are` 0.07 |
| 5 | ? ← is golden brown. | `␣it` | 0.088 | 3 | `␣crust` 0.20, `␣top` 0.13, `␣it` 0.09, `␣bread` 0.04, `␣cheese` 0.04 |
| 6 | ? ← it is golden brown… | `␣until` | 0.859 | 1 | `␣until` 0.86, `␣when` 0.05, `␣till` 0.03, `␣When` 0.01, `␣once` 0.01 |
| 7 | ? ← until it is golden… | `␣minutes` | 0.112 | 2 | `␣or` 0.33, `␣minutes` 0.11, `,` 0.08, `␣side` 0.04, `␣oil` 0.04 |
| 8 | ? ← minutes until it is… | `␣thirty` | 0.001 | 44 | `15` 0.13, `10` 0.12, `20` 0.10, `30` 0.09, `␣few` 0.08 |
| 9 | ? ← thirty minutes until it… | `␣for` | 0.279 | 1 | `␣for` 0.28, `␣to` 0.28, `␣about` 0.19, `␣every` 0.04, `␣another` 0.04 |
| 10 | ? ← for thirty minutes until… | `␣degrees` | 0.011 | 15 | `␣oven` 0.15, `␣bake` 0.11, `␣it` 0.08, `␣Bake` 0.05, `␣pan` 0.04 |
| 11 | ? ← degrees for thirty minutes… | `0` | 0.734 | 1 | `0` 0.73, `5` 0.24, `␣hundred` 0.00, `␣F` 0.00, `␣C` 0.00 |
| 12 | ? ← 0 degrees for thirty… | `22` | 0.001 | 22 | `35` 0.58, `40` 0.20, `45` 0.07, `30` 0.03, `18` 0.02 |
| 13 | ? ← 220 degrees for… | `␣` | 0.986 | 1 | `␣` 0.99, `-` 0.01, `/` 0.00, `,` 0.00, `␣at` 0.00 |
| 14 | ? ← 220 degrees… | `␣at` | 0.880 | 1 | `␣at` 0.88, `␣to` 0.02, `␣on` 0.02, `␣about` 0.01, `␣around` 0.01 |
| 15 | ? ← at 220… | `␣loaf` | 0.001 | 60 | `␣oven` 0.29, `␣bake` 0.14, `␣Bake` 0.13, `␣it` 0.10, `ake` 0.07 |
| 16 | ? ← loaf at 22… | `␣the` | 0.808 | 1 | `␣the` 0.81, `␣each` 0.03, `␣bread` 0.02, `␣entire` 0.01, `␣your` 0.01 |
| 17 | ? ← the loaf at… | `␣bake` | 0.281 | 2 | `␣Bake` 0.49, `␣bake` 0.28, `ake` 0.09, `␣baking` 0.03, `␣Baking` 0.02 |
| 18 | ? ← bake the loaf at… | `,` | 0.215 | 2 | `␣and` 0.45, `,` 0.22, `␣then` 0.11, `␣to` 0.06, `␣Then` 0.03 |
| 19 | ? ← , bake the loaf… | `␣Finally` | 0.106 | 1 | `␣Finally` 0.11, `␣oven` 0.08, `␣Then` 0.07, `␣baking` 0.04, `␣done` 0.03 |
| 20 | ? ← Finally, bake the… | `.` | 0.949 | 1 | `.` 0.95, `).` 0.02, `:` 0.00, `-` 0.00, `)` 0.00 |
| 21 | ? ← . Finally, bake… | `␣size` | 0.004 | 41 | `␣minutes` 0.04, `␣dough` 0.04, `␣pan` 0.03, `␣top` 0.03, `␣loaf` 0.02 |
| 22 | ? ← size. Finally,… | `␣in` | 0.643 | 1 | `␣in` 0.64, `␣desired` 0.10, `␣its` 0.03, `␣the` 0.02, `␣same` 0.02 |
| 23 | ? ← in size. Finally… | `␣doubled` | 0.463 | 1 | `␣doubled` 0.46, `␣doubles` 0.18, `␣double` 0.14, `␣uniform` 0.07, `␣equal` 0.04 |
| 24 | ? ← doubled in size.… | `␣has` | 0.397 | 1 | `␣has` 0.40, `␣until` 0.34, `␣is` 0.07, `␣have` 0.06, `␣almost` 0.04 |
| 25 | ? ← has doubled in size… | `␣it` | 0.824 | 1 | `␣it` 0.82, `␣dough` 0.08, `␣bread` 0.03, `␣loaf` 0.02, `␣and` 0.01 |
| 26 | ? ← it has doubled in… | `␣until` | 0.872 | 1 | `␣until` 0.87, `␣when` 0.03, `␣that` 0.03, `␣once` 0.02, `␣after` 0.02 |
| 27 | ? ← until it has doubled… | `␣hour` | 0.056 | 5 | `␣or` 0.47, `␣minutes` 0.15, `␣hours` 0.07, `␣rise` 0.07, `␣hour` 0.06 |
| 28 | ? ← hour until it has… | `␣an` | 0.423 | 1 | `␣an` 0.42, `␣one` 0.41, `␣another` 0.07, `␣every` 0.04, `␣half` 0.01 |
| 29 | ? ← an hour until it… | `␣for` | 0.439 | 1 | `␣for` 0.44, `␣half` 0.27, `␣about` 0.19, `␣to` 0.03, `␣least` 0.02 |
| 30 | ? ← for an hour until… | `␣rise` | 0.486 | 1 | `␣rise` 0.49, `␣place` 0.18, `␣dough` 0.03, `␣it` 0.03, `␣sit` 0.02 |
| 31 | ? ← rise for an hour… | `␣to` | 0.342 | 2 | `␣it` 0.37, `␣to` 0.34, `␣dough` 0.12, `␣bread` 0.06, `␣loaf` 0.04 |
| 32 | ? ← to rise for an… | `␣it` | 0.451 | 1 | `␣it` 0.45, `␣dough` 0.20, `␣bread` 0.09, `␣loaf` 0.04, `␣continue` 0.03 |
| 33 | ? ← it to rise for… | `␣leave` | 0.268 | 2 | `␣allow` 0.63, `␣leave` 0.27, `␣Allow` 0.04, `␣Leave` 0.02, `␣allowing` 0.01 |
| 34 | ? ← leave it to rise… | `␣then` | 0.082 | 3 | `␣and` 0.77, `,` 0.10, `␣then` 0.08, `␣Then` 0.02, `␣can` 0.00 |
| 35 | ? ← then leave it to… | `,` | 0.293 | 2 | `␣and` 0.66, `,` 0.29, `␣will` 0.01, `␣can` 0.01, `␣should` 0.00 |
| 36 | ? ← , then leave it… | `␣minutes` | 0.020 | 11 | `␣dough` 0.19, `␣wrap` 0.09, `␣cloth` 0.07, `␣towel` 0.05, `␣it` 0.05 |
| 37 | ? ← minutes, then leave… | `␣ten` | 0.119 | 2 | `␣thirty` 0.23, `␣twenty` 0.12, `30` 0.12, `␣ten` 0.12, `␣fifteen` 0.08 |
| 38 | ? ← ten minutes, then… | `␣for` | 0.809 | 1 | `␣for` 0.81, `␣about` 0.09, `␣another` 0.03, `␣around` 0.01, `␣every` 0.01 |
| 39 | ? ← for ten minutes,… | `␣dough` | 0.192 | 2 | `␣rise` 0.27, `␣dough` 0.19, `␣rest` 0.06, `␣it` 0.06, `␣place` 0.05 |
| 40 | ? ← dough for ten minutes… | `␣the` | 0.934 | 1 | `␣the` 0.93, `␣bread` 0.01, `␣of` 0.01, `␣your` 0.01, `␣risen` 0.01 |
| 41 | ? ← the dough for ten… | `ad` | 0.629 | 1 | `ad` 0.63, `ading` 0.10, `␣Cover` 0.03, `␣cover` 0.03, `erate` 0.02 |
| 42 | ? ← ad the dough for… | `ne` | 0.640 | 1 | `ne` 0.64, `␣kne` 0.36, `in` 0.00, `␣We` 0.00, `␣W` 0.00 |
| 43 | ? ← nead the dough… | `␣K` | 0.987 | 1 | `␣K` 0.99, `K` 0.01, `k` 0.00, `-K` 0.00, `.K` 0.00 |
| 44 | ? ← Knead the… | `.` | 0.982 | 1 | `.` 0.98, `).` 0.01, `:` 0.00, `.)` 0.00, `!` 0.00 |
| 45 | ? ← . Knead… | `␣bowl` | 0.042 | 3 | `␣dough` 0.13, `␣elastic` 0.05, `␣bowl` 0.04, `␣oil` 0.04, `␣it` 0.04 |
| 46 | ? ← bowl. Kne… | `␣large` | 0.131 | 4 | `␣a` 0.23, `␣the` 0.22, `ased` 0.14, `␣large` 0.13, `␣mixing` 0.05 |
| 47 | ? ← large bowl. K… | `␣a` | 0.955 | 1 | `␣a` 0.95, `␣the` 0.02, `␣or` 0.01, `␣another` 0.00, `␣one` 0.00 |
| 48 | ? ← a large bowl.… | `␣in` | 0.724 | 1 | `␣in` 0.72, `␣into` 0.18, `␣to` 0.03, `␣of` 0.02, `␣over` 0.01 |
| 49 | ? ← in a large bowl… | `␣water` | 0.033 | 9 | `␣salt` 0.15, `␣together` 0.15, `␣ingredients` 0.14, `␣it` 0.06, `␣yeast` 0.05 |
| 50 | ? ← water in a large… | `␣warm` | 0.093 | 3 | `␣and` 0.64, `␣of` 0.11, `␣warm` 0.09, `␣with` 0.04, `␣cold` 0.02 |
| 51 | ? ← warm water in a… | `␣and` | 0.538 | 1 | `␣and` 0.54, `␣of` 0.17, `␣with` 0.15, `␣the` 0.03, `␣some` 0.02 |
| 52 | ? ← and warm water in… | `␣salt` | 0.065 | 4 | `,` 0.44, `␣flour` 0.15, `␣yeast` 0.14, `␣salt` 0.07, `␣oil` 0.04 |
| 53 | ? ← salt and warm water… | `,` | 0.731 | 1 | `,` 0.73, `␣with` 0.11, `␣of` 0.06, `␣the` 0.03, `␣some` 0.01 |
| 54 | ? ← , salt and warm… | `␣yeast` | 0.312 | 1 | `␣yeast` 0.31, `␣flour` 0.30, `␣powder` 0.10, `␣sugar` 0.07, `␣oil` 0.05 |
| 55 | ? ← yeast, salt and… | `,` | 0.895 | 1 | `,` 0.90, `␣the` 0.03, `␣dry` 0.02, `␣with` 0.01, `␣of` 0.01 |
| 56 | ? ← , yeast, salt… | `␣flour` | 0.683 | 1 | `␣flour` 0.68, `␣sugar` 0.14, `␣powder` 0.04, `our` 0.01, `␣salt` 0.01 |
| 57 | ? ← flour, yeast,… | `␣the` | 0.341 | 1 | `␣the` 0.34, `,` 0.11, `␣combine` 0.07, `␣bread` 0.07, `␣of` 0.05 |
| 58 | ? ← the flour, yeast… | `␣mix` | 0.171 | 2 | `␣combine` 0.31, `␣mix` 0.17, `␣together` 0.11, `␣Combine` 0.10, `␣place` 0.07 |
| 59 | ? ← mix the flour,… | `,` | 0.814 | 1 | `,` 0.81, `␣to` 0.06, `␣simply` 0.03, `␣first` 0.02, `␣Simply` 0.02 |
| 60 | ? ← , mix the flour… | `First` | 0.023 | 11 | `␣dough` 0.16, `␣Next` 0.11, `␣bread` 0.09, `␣First` 0.09, `␣loaf` 0.06 |

---

## 6. moon_landing

*Category: temporal*

> **Beginning:** Apollo 11 launched from Kennedy Space Center on July 16, 1969.  
> **Middle:** Four days later, the lunar module Eagle separated from the command module and descended to the surface.  
> **Ending:** Neil Armstrong then became the first person to walk on the Moon.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | first person to walk on the moon. ↵ On July 20, 1969, Neil Armstrong became the first person to walk on the moon. ↵ On July 20, 1969, Neil Armstrong became the first person to walk on the moon. ↵ On July 20, 1969, Neil Armstrong became the first person to walk on the moon. ↵ On July 20, 1969, Neil Armstrong became the first person to walk on the moon. ↵ | Neil Armstrong then became the first person to walk on the Moon. |
| sample | , Neil Armstrong and Buzz Aldrin took part in a U.S. space program called Gemini 11 and Apollo 11, one of the longest space missions in history. ↵  ↵ Apollo 11 ↵ Apollo 11, Neil Armstrong, Neil Armstrong and U.S. astronaut, Neil Armstrong, made the trip to the moon. ↵  ↵ Apollo 11 ↵ Apollo 11, Apollo 11, Neil Armstrong and Buzz Aldrin walked on the moon. ↵ | Neil Armstrong then became the first person to walk on the Moon. |
| sample | revolutionary discovery that changed the world of space exploration at the end of the 20th century. ↵  ↵ But perhaps the most significant moment in history comes in 2019 with the discovery of American astronaut Neil Armstrong (Apollo 11). Astronaut Neil Armstrong flew into space aboard a Saturn V rocket and made a historic landing on a planet 300 million miles away from Earth in the 1920s. This discovery had a significant impact on the future of space exploration. ↵  ↵ | Neil Armstrong then became the first person to walk on the Moon. |
| sample | (32.2°F) for five months of the year. ↵  ↵ Who Was The First Man On The Moon? ↵  ↵ Neil Armstrong was the first man on the moon since Apollo 15, when Neil Armstrong landed on the surface of the moon. The first photograph of the lunar surface was taken by astronaut Neil Armstrong during the launch of Apollo 11. Three days after the launch of Apollo 11, Lance Armstrong left a record of people going to the moon. ↵  ↵ | Neil Armstrong then became the first person to walk on the Moon. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | Apollo 11 launched from Kennedy Space Center on July 16, 1969. | The mission was a success, but it was also a failure. The Apollo 11 mission was a success, but it was also a failure. The Apollo 11 mission was a success, but it was also a failure. The Apollo 11 mission was a success, but it was also a failure. The Apollo 11 mission was a success, but it was also a failure. The Apollo 11 mission was a success, but it was also a failure. The Apollo |
| sample | Apollo 11 launched from Kennedy Space Center on July 16, 1969. | The mission began as an initial plan to visit the moon, but did not complete the planned mission because it was too small for the Apollo 11 crew. When the Apollo 11 crew made their last leg on January 21, 1969, they were given a new mission: to visit another planet. ↵ The first mission was to visit the moon. The moon is very close to the Earth and it takes only about three minutes to get there. The mission was to test the |
| sample | Apollo 11 launched from Kennedy Space Center on July 16, 1969. | It was the first American space shuttle, and was designated the "first major manned flight" in aviation history. The shuttle was designed by Theodore Shultz, and was a success. It was used in a number of space missions, including the first shuttle landing on Mars, and the first successful spaceflight after Columbia. The launch of Apollo 11 was a historic moment for American space exploration, and has been a source of pride for the United States since the program |
| sample | Apollo 11 launched from Kennedy Space Center on July 16, 1969. | It was the first manned space mission to launch a man-made mission in space. It was the first manned mission to launch a man-made mission into space. The Apollo 11 mission was intended to be the first manned orbital mission to enter space on a mission to a planet outside our solar system. This mission also brought humanity to the Moon. The Apollo 11 mission was an important milestone in the field of space exploration. It also brought the first humans to venture into |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.658 | 57% |
| Backward | previous-token (right context) | 0.628 | 57% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `Ap` | 0.000 | 728 | `The` 0.06, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | Ap → ? | `ollo` | 0.093 | 2 | `pe` 0.14, `pearance` 0.09, `ollo` 0.09, `ache` 0.08, `ologies` 0.05 |
| 3 | Apollo → ? | `␣` | 0.540 | 1 | `␣` 0.54, `'s` 0.03, `␣Mission` 0.01, `\n\n` 0.01, `,` 0.01 |
| 4 | Apollo → ? | `11` | 0.307 | 1 | `11` 0.31, `13` 0.15, `8` 0.08, `17` 0.07, `10` 0.06 |
| 5 | Apollo 11 → ? | `␣launched` | 0.003 | 39 | `␣was` 0.09, `:` 0.09, `\n\n` 0.04, `,` 0.04, `\n` 0.04 |
| 6 | …ollo 11 launched → ? | `␣from` | 0.060 | 3 | `␣on` 0.42, `␣in` 0.14, `␣from` 0.06, `␣` 0.04, `␣a` 0.03 |
| 7 | …11 launched from → ? | `␣Kennedy` | 0.116 | 3 | `␣the` 0.38, `␣Cape` 0.20, `␣Kennedy` 0.12, `␣a` 0.05, `␣Houston` 0.02 |
| 8 | …11 launched from Kennedy → ? | `␣Space` | 0.924 | 1 | `␣Space` 0.92, `'s` 0.04, `␣Launch` 0.01, `␣space` 0.00, `Space` 0.00 |
| 9 | …launched from Kennedy Space → ? | `␣Center` | 0.968 | 1 | `␣Center` 0.97, `␣Centre` 0.01, `␣Flight` 0.01, `␣Station` 0.00, `Center` 0.00 |
| 10 | …from Kennedy Space Center → ? | `␣on` | 0.233 | 2 | `␣in` 0.33, `␣on` 0.23, `,` 0.08, `'s` 0.08, `␣at` 0.03 |
| 11 | …Kennedy Space Center on → ? | `␣July` | 0.138 | 1 | `␣July` 0.14, `␣April` 0.07, `␣November` 0.07, `␣May` 0.06, `␣January` 0.06 |
| 12 | …Space Center on July → ? | `␣` | 0.996 | 1 | `␣` 1.00, `\n` 0.00, `,` 0.00, `\n\n` 0.00, `.` 0.00 |
| 13 | …Center on July → ? | `16` | 0.047 | 7 | `10` 0.07, `11` 0.06, `14` 0.05, `12` 0.05, `20` 0.05 |
| 14 | …on July 16 → ? | `,` | 0.830 | 1 | `,` 0.83, `th` 0.07, `␣at` 0.02, `.` 0.02, `␣and` 0.01 |
| 15 | …July 16, → ? | `␣` | 0.971 | 1 | `␣` 0.97, `␣carrying` 0.01, `␣and` 0.00, `␣the` 0.00, `19` 0.00 |
| 16 | …16, → ? | `19` | 0.983 | 1 | `19` 0.98, `20` 0.02, `11` 0.00, `17` 0.00, `18` 0.00 |
| 17 | …16, 19 → ? | `69` | 0.322 | 1 | `69` 0.32, `61` 0.17, `67` 0.15, `62` 0.07, `68` 0.07 |
| 18 | …, 1969 → ? | `.` | 0.374 | 1 | `.` 0.37, `,` 0.37, `␣and` 0.05, `␣as` 0.03, `␣with` 0.02 |
| 19 | …1969. → ? | `␣Four` | 0.003 | 27 | `␣The` 0.27, `␣It` 0.24, `␣This` 0.03, `␣Its` 0.02, `␣On` 0.02 |
| 20 | …1969. Four → ? | `␣days` | 0.165 | 2 | `␣years` 0.25, `␣days` 0.17, `␣months` 0.12, `␣astronauts` 0.10, `teen` 0.06 |
| 21 | …69. Four days → ? | `␣later` | 0.556 | 1 | `␣later` 0.56, `␣after` 0.29, `␣before` 0.04, `␣and` 0.04, `␣into` 0.02 |
| 22 | …. Four days later → ? | `,` | 0.622 | 1 | `,` 0.62, `␣on` 0.09, `␣the` 0.08, `␣Apollo` 0.06, `␣it` 0.04 |
| 23 | …Four days later, → ? | `␣the` | 0.272 | 1 | `␣the` 0.27, `␣on` 0.20, `␣Apollo` 0.10, `␣it` 0.08, `␣Neil` 0.03 |
| 24 | …days later, the → ? | `␣lunar` | 0.005 | 27 | `␣Apollo` 0.12, `␣first` 0.09, `␣spacecraft` 0.06, `␣crew` 0.06, `␣space` 0.05 |
| 25 | …later, the lunar → ? | `␣module` | 0.256 | 2 | `␣land` 0.32, `␣module` 0.26, `␣landing` 0.20, `␣orbit` 0.02, `␣surface` 0.02 |
| 26 | …, the lunar module → ? | `␣Eagle` | 0.003 | 37 | `␣was` 0.18, `␣landed` 0.09, `,` 0.07, `␣Apollo` 0.04, `␣returned` 0.04 |
| 27 | …the lunar module Eagle → ? | `␣separated` | 0.000 | 732 | `␣landed` 0.52, `␣launched` 0.04, `␣flew` 0.03, `␣touched` 0.03, `␣was` 0.03 |
| 28 | …lunar module Eagle separated → ? | `␣from` | 0.918 | 1 | `␣from` 0.92, `␣into` 0.01, `␣and` 0.01, `␣on` 0.01, `␣itself` 0.01 |
| 29 | …module Eagle separated from → ? | `␣the` | 0.616 | 1 | `␣the` 0.62, `␣its` 0.12, `␣Apollo` 0.08, `␣Earth` 0.04, `␣Kennedy` 0.02 |
| 30 | …Eagle separated from the → ? | `␣command` | 0.005 | 25 | `␣Apollo` 0.17, `␣lunar` 0.10, `␣landing` 0.07, `␣rocket` 0.05, `␣spacecraft` 0.05 |
| 31 | …separated from the command → ? | `␣module` | 0.898 | 1 | `␣module` 0.90, `␣Module` 0.01, `ing` 0.01, `␣capsule` 0.01, `␣post` 0.01 |
| 32 | …from the command module → ? | `␣and` | 0.011 | 15 | `␣Apollo` 0.13, `␣Eagle` 0.07, `,` 0.07, `␣Columbia` 0.04, `␣Arm` 0.03 |
| 33 | …the command module and → ? | `␣descended` | 0.007 | 18 | `␣landed` 0.11, `␣the` 0.06, `␣became` 0.05, `␣entered` 0.04, `␣returned` 0.04 |
| 34 | …command module and descended → ? | `␣to` | 0.385 | 1 | `␣to` 0.38, `␣into` 0.29, `␣on` 0.07, `␣onto` 0.04, `␣` 0.02 |
| 35 | …module and descended to → ? | `␣the` | 0.457 | 1 | `␣the` 0.46, `␣a` 0.16, `␣Earth` 0.10, `␣` 0.04, `␣earth` 0.04 |
| 36 | …and descended to the → ? | `␣surface` | 0.352 | 1 | `␣surface` 0.35, `␣moon` 0.18, `␣Moon` 0.15, `␣lunar` 0.15, `␣bottom` 0.03 |
| 37 | …descended to the surface → ? | `.` | 0.166 | 2 | `␣of` 0.49, `.` 0.17, `,` 0.09, `␣on` 0.03, `␣for` 0.03 |
| 38 | …to the surface. → ? | `␣Neil` | 0.007 | 20 | `␣The` 0.23, `␣Apollo` 0.08, `␣It` 0.06, `␣On` 0.04, `␣Eagle` 0.04 |
| 39 | …the surface. Neil → ? | `␣Arm` | 0.955 | 1 | `␣Arm` 0.95, `␣A` 0.01, `␣de` 0.00, `␣and` 0.00, `␣Young` 0.00 |
| 40 | …surface. Neil Arm → ? | `strong` | 0.999 | 1 | `strong` 1.00, `st` 0.00, `and` 0.00, `man` 0.00, `cro` 0.00 |
| 41 | …. Neil Armstrong → ? | `␣then` | 0.004 | 24 | `,` 0.17, `␣and` 0.16, `␣was` 0.11, `␣became` 0.04, `␣stepped` 0.04 |
| 42 | …Neil Armstrong then → ? | `␣became` | 0.051 | 6 | `␣set` 0.11, `␣walked` 0.09, `␣stepped` 0.08, `␣took` 0.06, `␣landed` 0.05 |
| 43 | …Armstrong then became → ? | `␣the` | 0.931 | 1 | `␣the` 0.93, `␣one` 0.02, `␣history` 0.01, `␣a` 0.00, `␣known` 0.00 |
| 44 | …strong then became the → ? | `␣first` | 0.942 | 1 | `␣first` 0.94, `␣most` 0.01, `␣commander` 0.01, `␣world` 0.00, `␣greatest` 0.00 |
| 45 | …then became the first → ? | `␣person` | 0.104 | 3 | `␣man` 0.53, `␣human` 0.25, `␣person` 0.10, `␣American` 0.05, `␣commander` 0.01 |
| 46 | …became the first person → ? | `␣to` | 0.823 | 1 | `␣to` 0.82, `␣in` 0.07, `␣on` 0.05, `␣ever` 0.03, `,` 0.01 |
| 47 | …the first person to → ? | `␣walk` | 0.439 | 1 | `␣walk` 0.44, `␣set` 0.32, `␣step` 0.06, `␣land` 0.03, `␣be` 0.03 |
| 48 | …first person to walk → ? | `␣on` | 0.965 | 1 | `␣on` 0.96, `␣the` 0.01, `␣over` 0.00, `␣upon` 0.00, `␣across` 0.00 |
| 49 | …person to walk on → ? | `␣the` | 0.968 | 1 | `␣the` 0.97, `␣another` 0.01, `␣moon` 0.01, `␣lunar` 0.00, `␣a` 0.00 |
| 50 | …to walk on the → ? | `␣Moon` | 0.134 | 3 | `␣moon` 0.64, `␣surface` 0.18, `␣Moon` 0.13, `␣lunar` 0.04, `␣other` 0.00 |
| 51 | …walk on the Moon → ? | `.` | 0.431 | 1 | `.` 0.43, `,` 0.13, `.\n` 0.08, `␣in` 0.08, `␣and` 0.04 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.519 | 1 | `.` 0.52, `!` 0.03, `)` 0.02, `).` 0.01, `?` 0.01 |
| 2 | ? ← . | `␣Moon` | 0.000 | 5481 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣Yes` 0.00, `␣years` 0.00 |
| 3 | ? ← Moon. | `␣the` | 0.686 | 1 | `␣the` 0.69, `␣The` 0.06, `␣Full` 0.03, `␣and` 0.03, `␣full` 0.02 |
| 4 | ? ← the Moon. | `␣on` | 0.289 | 1 | `␣on` 0.29, `␣of` 0.24, `␣to` 0.16, `␣and` 0.07, `␣from` 0.04 |
| 5 | ? ← on the Moon. | `␣walk` | 0.017 | 6 | `␣land` 0.04, `␣water` 0.03, `␣man` 0.03, `␣life` 0.02, `␣humans` 0.02 |
| 6 | ? ← walk on the Moon… | `␣to` | 0.610 | 1 | `␣to` 0.61, `␣can` 0.03, `␣could` 0.03, `␣and` 0.03, `␣To` 0.02 |
| 7 | ? ← to walk on the… | `␣person` | 0.159 | 1 | `␣person` 0.16, `␣man` 0.12, `␣woman` 0.09, `␣humans` 0.08, `␣human` 0.07 |
| 8 | ? ← person to walk on… | `␣first` | 0.868 | 1 | `␣first` 0.87, `␣third` 0.02, `␣last` 0.02, `␣second` 0.01, `th` 0.01 |
| 9 | ? ← first person to walk… | `␣the` | 0.902 | 1 | `␣the` 0.90, `␣The` 0.09, `'s` 0.00, `␣very` 0.00, `␣and` 0.00 |
| 10 | ? ← the first person to… | `␣became` | 0.197 | 2 | `␣was` 0.37, `␣became` 0.20, `␣be` 0.08, `␣become` 0.06, `,` 0.05 |
| 11 | ? ← became the first person… | `␣then` | 0.001 | 105 | `strong` 0.15, `␣who` 0.12, `␣he` 0.08, `␣He` 0.07, `␣and` 0.06 |
| 12 | ? ← then became the first… | `strong` | 0.003 | 9 | `␣and` 0.38, `␣who` 0.27, `␣He` 0.12, `,` 0.06, `␣he` 0.03 |
| 13 | ? ← strong then became the… | `␣Arm` | 0.984 | 1 | `␣Arm` 0.98, `m` 0.02, `\n` 0.00, `␣L` 0.00, `␣W` 0.00 |
| 14 | ? ← Armstrong then became… | `␣Neil` | 0.598 | 1 | `␣Neil` 0.60, `.` 0.13, `il` 0.06, `win` 0.04, `,` 0.04 |
| 15 | ? ← Neil Armstrong then… | `.` | 0.436 | 1 | `.` 0.44, `:` 0.26, `,` 0.08, `␣and` 0.04, `␣astronaut` 0.02 |
| 16 | ? ← . Neil Armstrong… | `␣surface` | 0.048 | 3 | `␣moon` 0.08, `␣Moon` 0.06, `␣surface` 0.05, `11` 0.04, `␣landing` 0.04 |
| 17 | ? ← surface. Neil Arm… | `␣the` | 0.177 | 3 | `␣lunar` 0.46, `'s` 0.22, `␣the` 0.18, `’s` 0.05, `␣its` 0.03 |
| 18 | ? ← the surface. Neil… | `␣to` | 0.197 | 2 | `␣on` 0.40, `␣to` 0.20, `␣above` 0.06, `␣from` 0.05, `␣below` 0.05 |
| 19 | ? ← to the surface.… | `␣descended` | 0.042 | 4 | `␣back` 0.07, `␣return` 0.07, `␣returned` 0.05, `␣descended` 0.04, `␣astronauts` 0.04 |
| 20 | ? ← descended to the surface… | `␣and` | 0.277 | 1 | `␣and` 0.28, `␣then` 0.05, `strong` 0.05, `,` 0.04, `rin` 0.03 |
| 21 | ? ← and descended to the… | `␣module` | 0.015 | 13 | `,` 0.11, `␣surface` 0.03, `␣landing` 0.03, `␣moon` 0.03, `␣Earth` 0.02 |
| 22 | ? ← module and descended to… | `␣command` | 0.077 | 3 | `␣lunar` 0.53, `␣the` 0.20, `␣command` 0.08, `11` 0.03, `␣landing` 0.01 |
| 23 | ? ← command module and descended… | `␣the` | 0.579 | 1 | `␣the` 0.58, `'s` 0.06, `␣lunar` 0.05, `␣Apollo` 0.05, `11` 0.04 |
| 24 | ? ← the command module and… | `␣from` | 0.348 | 1 | `␣from` 0.35, `␣to` 0.09, `␣of` 0.06, `␣in` 0.06, `␣on` 0.05 |
| 25 | ? ← from the command module… | `␣separated` | 0.107 | 2 | `␣off` 0.11, `␣separated` 0.11, `␣launched` 0.05, `ed` 0.04, `␣detached` 0.04 |
| 26 | ? ← separated from the command… | `␣Eagle` | 0.004 | 37 | `strong` 0.11, `,` 0.09, `␣was` 0.05, `rin` 0.05, `␣he` 0.04 |
| 27 | ? ← Eagle separated from the… | `␣module` | 0.195 | 1 | `␣module` 0.19, `␣American` 0.18, `␣the` 0.15, `␣Module` 0.08, `,` 0.07 |
| 28 | ? ← module Eagle separated from… | `␣lunar` | 0.603 | 1 | `␣lunar` 0.60, `␣command` 0.23, `␣control` 0.03, `␣the` 0.02, `␣landing` 0.01 |
| 29 | ? ← lunar module Eagle separated… | `␣the` | 0.772 | 1 | `␣the` 0.77, `␣The` 0.07, `␣first` 0.01, `␣in` 0.01, `'s` 0.01 |
| 30 | ? ← the lunar module Eagle… | `,` | 0.451 | 1 | `,` 0.45, `␣when` 0.19, `␣on` 0.06, `␣of` 0.04, `␣from` 0.02 |
| 31 | ? ← , the lunar module… | `␣later` | 0.046 | 4 | `11` 0.08, `69` 0.06, `␣landing` 0.05, `␣later` 0.05, `␣mission` 0.03 |
| 32 | ? ← later, the lunar… | `␣days` | 0.283 | 1 | `␣days` 0.28, `␣minutes` 0.27, `␣hours` 0.14, `␣hour` 0.06, `␣seconds` 0.04 |
| 33 | ? ← days later, the… | `␣Four` | 0.075 | 3 | `␣Two` 0.12, `␣Three` 0.08, `␣Four` 0.08, `␣few` 0.06, `␣two` 0.06 |
| 34 | ? ← Four days later,… | `.` | 0.942 | 1 | `.` 0.94, `).` 0.01, `."` 0.01, `:` 0.01, `".` 0.00 |
| 35 | ? ← . Four days later… | `69` | 0.015 | 10 | `␣moon` 0.08, `␣surface` 0.07, `␣Moon` 0.06, `11` 0.04, `␣Earth` 0.03 |
| 36 | ? ← 69. Four days… | `19` | 0.972 | 1 | `19` 0.97, `␣` 0.02, `-` 0.01, `11` 0.00, `15` 0.00 |
| 37 | ? ← 1969. Four… | `␣` | 0.992 | 1 | `␣` 0.99, `,` 0.01, `-` 0.00, `.` 0.00, `␣July` 0.00 |
| 38 | ? ← 1969.… | `,` | 0.805 | 1 | `,` 0.81, `␣July` 0.08, `␣in` 0.02, `␣August` 0.01, `␣January` 0.01 |
| 39 | ? ← , 1969… | `16` | 0.035 | 7 | `20` 0.09, `11` 0.06, `15` 0.05, `17` 0.04, `21` 0.04 |
| 40 | ? ← 16, 19… | `␣` | 0.995 | 1 | `␣` 1.00, `-` 0.00, `–` 0.00, `20` 0.00, `.` 0.00 |
| 41 | ? ← 16,… | `␣July` | 0.760 | 1 | `␣July` 0.76, `.` 0.09, `␣August` 0.02, `␣March` 0.02, `␣May` 0.01 |
| 42 | ? ← July 16,… | `␣on` | 0.894 | 1 | `␣on` 0.89, `,` 0.05, `␣of` 0.02, `␣moon` 0.01, `␣landing` 0.00 |
| 43 | ? ← on July 16… | `␣Center` | 0.001 | 92 | `␣moon` 0.21, `␣Moon` 0.09, `,` 0.07, `␣landing` 0.07, `␣surface` 0.04 |
| 44 | ? ← Center on July… | `␣Space` | 0.664 | 1 | `␣Space` 0.66, `␣Trade` 0.14, `␣Research` 0.05, `␣Test` 0.04, `␣Launch` 0.02 |
| 45 | ? ← Space Center on July… | `␣Kennedy` | 0.935 | 1 | `␣Kennedy` 0.94, `␣Johnson` 0.06, `ennis` 0.00, `nedy` 0.00, `␣the` 0.00 |
| 46 | ? ← Kennedy Space Center on… | `␣from` | 0.100 | 4 | `␣the` 0.49, `␣at` 0.16, `'s` 0.14, `␣from` 0.10, `␣to` 0.03 |
| 47 | ? ← from Kennedy Space Center… | `␣launched` | 0.247 | 2 | `␣off` 0.49, `␣launched` 0.25, `␣rocket` 0.03, `␣launch` 0.02, `ed` 0.02 |
| 48 | ? ← launched from Kennedy Space… | `11` | 0.002 | 32 | `␣was` 0.57, `␣and` 0.07, `␣were` 0.05, `,` 0.04, `␣Eagle` 0.03 |
| 49 | ? ← 11 launched from Kennedy… | `␣` | 0.859 | 1 | `␣` 0.86, `-` 0.14, `11` 0.00, `10` 0.00, `.` 0.00 |
| 50 | ? ← 11 launched from… | `ollo` | 0.128 | 2 | `␣Apollo` 0.84, `ollo` 0.13, `ition` 0.01, `at` 0.00, `is` 0.00 |
| 51 | ? ← ollo 11 launched… | `Ap` | 0.973 | 1 | `Ap` 0.97, `p` 0.02, `␣ap` 0.00, `␣Ap` 0.00, `ap` 0.00 |

---

## 7. socrates

*Category: logical*

> **Beginning:** All men are mortal.  
> **Middle:** Socrates is a man.  
> **Ending:** Therefore, Socrates is mortal.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ Therefore, Socrates is mortal. ↵ | Therefore, Socrates is mortal. |
| sample | ↵ - true true false ↵ - true true false ↵ - true true false ↵ - true true false ↵ - true true false ↵ - true true false ↵ - true true false ↵ - true true false ↵ - true true false ↵ - true true false ↵ - Socrates is a man. ↵ - A man is mortal. ↵ - Therefore, Socrates is mortal. ↵ - A man is mortal. ↵ Therefore, Socrates is mortal. ↵ - A man is mortal. ↵ | Therefore, Socrates is mortal. |
| sample | Socrates is a mortal. ↵ Socrates Therefore Socrates is a mortal. ↵ Mortal Socrates is a mortal is a mortal. ↵ Mortal Socrates is a mortal is a mortal. ↵ Socrates Socrates is a mortal. ↵ Socrates Therefore Socrates is mortal. ↵ Socrates Therefore, Socrates is mortal. ↵ Socrates is a mortal - Alcrates is a mortal of Socrates ↵ | Therefore, Socrates is mortal. |
| sample | rates be if you die? ↵ (a) ↵ You're going to die ↵ (b) ↵ You're going to die ↵ (c) ↵ You're going to die ↵ (d) ↵ You're going to die ↵ (e) ↵ If you die, you're going to die. If you die, you die. If you die, you're going to die. If you die, you're going to die. You're going to die. Hence, Socrates is mortal ↵ | Therefore, Socrates is mortal. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | All men are mortal. | They are mortal because they are mortal. They are mortal because they are mortal. They are mortal because they are mortal. They are mortal because they are mortal. They are mortal because they are mortal. They are mortal because they are mortal. They are mortal because they are mortal. They are mortal because they are mortal. They are mortal because they are mortal. They are mortal because they |
| sample | All men are mortal. | They are immortal, yet there is a divide between men and women. Some men and women share their soul, others share their spirit. Only the Gods of the soul can speak. The soul is not in the body of the dead, the body of the living. The soul is not on the mind of the dead, the body of the living. The soul is not in the eye of the dead, the body of the living. The soul must be on the part |
| sample | All men are mortal. | So when a man's life is affected by the lack of food, water, and rest, his entire existence is ruined. This is why one must practice food for life. But the food they eat is not the only food they eat. All those other foods are also food. They are all food. ↵ We must practice food for life. Food for life is the most important part of our diet. It is the foundation of our existence and the root of our survival. It is |
| sample | All men are mortal. | All men are mortal. All men are mortal. Men can be mortal. All men are mortal. ↵ The word "mortal" means "man." It's a reference to the fact that men are the rulers of the world around them. Men are the rulers of the world. ↵ Men are the rulers of the world. They are the rulers of the world because they live in the world. The world is the world because men are the |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.907 | 55% |
| Backward | previous-token (right context) | 0.770 | 45% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `All` | 0.002 | 72 | `The` 0.06, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | All → ? | `␣men` | 0.001 | 111 | `␣About` 0.09, `␣of` 0.06, `␣the` 0.06, `␣about` 0.05, `␣you` 0.04 |
| 3 | All men → ? | `␣are` | 0.164 | 1 | `␣are` 0.16, `␣have` 0.09, `,` 0.08, `␣and` 0.07, `␣should` 0.05 |
| 4 | All men are → ? | `␣mort` | 0.006 | 21 | `␣born` 0.13, `␣not` 0.09, `␣created` 0.05, `␣different` 0.04, `␣equal` 0.04 |
| 5 | All men are mort → ? | `al` | 0.927 | 1 | `al` 0.93, `als` 0.03, `ified` 0.02, `ally` 0.01, `g` 0.01 |
| 6 | …men are mortal → ? | `.` | 0.201 | 2 | `,` 0.21, `.` 0.20, `␣and` 0.12, `␣enemies` 0.05, `;` 0.05 |
| 7 | …are mortal. → ? | `␣Soc` | 0.003 | 54 | `␣They` 0.09, `␣All` 0.07, `␣The` 0.05, `␣But` 0.04, `␣And` 0.04 |
| 8 | …mortal. Soc → ? | `rates` | 0.962 | 1 | `rates` 0.96, `io` 0.02, `cer` 0.00, `rate` 0.00, `ius` 0.00 |
| 9 | …al. Socrates → ? | `␣is` | 0.132 | 2 | `,` 0.16, `␣is` 0.13, `␣was` 0.11, `␣said` 0.07, `\n` 0.03 |
| 10 | …. Socrates is → ? | `␣a` | 0.143 | 2 | `␣mort` 0.29, `␣a` 0.14, `␣the` 0.10, `␣not` 0.10, `␣Soc` 0.02 |
| 11 | …Socrates is a → ? | `␣man` | 0.383 | 1 | `␣man` 0.38, `␣mort` 0.27, `␣human` 0.01, `␣male` 0.01, `␣myth` 0.01 |
| 12 | …rates is a man → ? | `.` | 0.227 | 2 | `,` 0.26, `.` 0.23, `␣of` 0.13, `␣who` 0.07, `␣and` 0.04 |
| 13 | …is a man. → ? | `␣Therefore` | 0.008 | 22 | `␣He` 0.09, `␣Soc` 0.07, `␣The` 0.05, `␣Men` 0.04, `␣All` 0.04 |
| 14 | …a man. Therefore → ? | `,` | 0.430 | 1 | `,` 0.43, `␣Soc` 0.15, `␣is` 0.09, `␣he` 0.04, `␣are` 0.03 |
| 15 | …man. Therefore, → ? | `␣Soc` | 0.169 | 1 | `␣Soc` 0.17, `␣he` 0.11, `␣all` 0.08, `␣the` 0.06, `␣men` 0.05 |
| 16 | …. Therefore, Soc → ? | `rates` | 0.994 | 1 | `rates` 0.99, `rate` 0.01, `R` 0.00, `ius` 0.00, `op` 0.00 |
| 17 | …Therefore, Socrates → ? | `␣is` | 0.782 | 1 | `␣is` 0.78, `␣must` 0.03, `␣was` 0.02, `,` 0.01, `␣has` 0.01 |
| 18 | …, Socrates is → ? | `␣mort` | 0.364 | 1 | `␣mort` 0.36, `␣a` 0.36, `␣the` 0.03, `␣not` 0.03, `␣also` 0.02 |
| 19 | …Socrates is mort → ? | `al` | 0.997 | 1 | `al` 1.00, `ally` 0.00, `als` 0.00, `all` 0.00, `ified` 0.00 |
| 20 | …rates is mortal → ? | `.` | 0.517 | 1 | `.` 0.52, `.\n` 0.09, `,` 0.09, `␣too` 0.07, `.\n\n` 0.06 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.519 | 1 | `.` 0.52, `!` 0.03, `)` 0.02, `).` 0.01, `?` 0.01 |
| 2 | ? ← . | `al` | 0.000 | 618 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣Yes` 0.00, `␣years` 0.00 |
| 3 | ? ← al. | `␣mort` | 0.003 | 67 | `␣Port` 0.05, `␣Med` 0.03, `de` 0.03, `␣pedest` 0.03, `␣fo` 0.03 |
| 4 | ? ← mortal. | `␣is` | 0.094 | 3 | `␣mere` 0.20, `␣a` 0.17, `␣is` 0.09, `␣are` 0.06, `␣the` 0.03 |
| 5 | ? ← is mortal. | `rates` | 0.113 | 1 | `␣he` 0.11, `rates` 0.11, `␣man` 0.04, `␣who` 0.04, `␣He` 0.03 |
| 6 | ? ← rates is mortal… | `␣Soc` | 0.921 | 1 | `␣Soc` 0.92, `oc` 0.04, `ph` 0.01, `␣soc` 0.01, `ist` 0.01 |
| 7 | ? ← Socrates is mort… | `,` | 0.202 | 2 | `␣that` 0.28, `:` 0.20, `,` 0.20, `.` 0.03, `␣and` 0.03 |
| 8 | ? ← , Socrates is… | `␣Therefore` | 0.046 | 3 | `␣Yes` 0.35, `␣No` 0.28, `␣Therefore` 0.05, `rates` 0.03, `␣Thus` 0.03 |
| 9 | ? ← Therefore, Socrates… | `.` | 0.657 | 1 | `.` 0.66, `:` 0.22, `).` 0.02, `)` 0.02, `."` 0.01 |
| 10 | ? ← . Therefore, Soc… | `␣man` | 0.040 | 3 | `al` 0.31, `rates` 0.17, `␣man` 0.04, `␣men` 0.03, `on` 0.01 |
| 11 | ? ← man. Therefore,… | `␣a` | 0.519 | 1 | `␣a` 0.52, `al` 0.09, `␣is` 0.06, `rates` 0.03, `␣of` 0.03 |
| 12 | ? ← a man. Therefore… | `␣is` | 0.532 | 1 | `␣is` 0.53, `␣of` 0.05, `rates` 0.04, `␣not` 0.04, `␣be` 0.03 |
| 13 | ? ← is a man.… | `rates` | 0.598 | 1 | `rates` 0.60, `al` 0.09, `␣man` 0.08, `␣he` 0.07, `,` 0.02 |
| 14 | ? ← rates is a man… | `␣Soc` | 0.994 | 1 | `␣Soc` 0.99, `oc` 0.00, `c` 0.00, `␣soc` 0.00, `␣Men` 0.00 |
| 15 | ? ← Socrates is a… | `.` | 0.195 | 2 | `,` 0.24, `.` 0.20, `␣that` 0.14, `:` 0.05, `␣and` 0.04 |
| 16 | ? ← . Socrates is… | `al` | 0.215 | 2 | `␣man` 0.23, `al` 0.22, `rates` 0.14, `␣men` 0.05, `2` 0.01 |
| 17 | ? ← al. Socrates… | `␣mort` | 0.940 | 1 | `␣mort` 0.94, `␣immort` 0.05, `␣Mort` 0.00, `ort` 0.00, `␣prim` 0.00 |
| 18 | ? ← mortal. Soc… | `␣are` | 0.237 | 2 | `␣is` 0.60, `␣are` 0.24, `␣a` 0.04, `␣not` 0.02, `␣both` 0.01 |
| 19 | ? ← are mortal.… | `␣men` | 0.305 | 2 | `rates` 0.38, `␣men` 0.31, `␣Men` 0.03, `␣both` 0.03, `es` 0.02 |
| 20 | ? ← men are mortal… | `All` | 0.203 | 2 | `␣All` 0.42, `All` 0.20, `␣all` 0.17, `␣Both` 0.04, `,` 0.02 |

---

## 8. even_numbers

*Category: logical*

> **Beginning:** An even number is any integer that can be divided by two without a remainder.  
> **Middle:** If we add two even numbers, each can be written as two times some integer, so their sum is two times the sum of those integers.  
> **Ending:** This proves that the sum of two even numbers is always even.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | two even numbers is even. ↵ From the formula above, we can see that the sum of two even numbers is even. ↵ From the formula above, we can see that the sum of two even numbers is even. ↵ From the formula above, we can see that the sum of two even numbers is even. ↵ From the formula above, we can see that the sum of two even numbers is even. ↵ From the formula above, we can see that the sum of two even numbers is even. ↵ | This proves that the sum of two even numbers is always even. |
| sample | two even numbers is even than 1. ↵ We also know that the sum of two odd numbers is even than 0. ↵ Therefore, we know that the sum of two odd numbers are greater than 0. ↵ Similarly, we know that the sum of two even numbers is even than 0. ↵ Therefore, we know that the sum of two even numbers is greater than 1 or even greater than 0. ↵ Finally, we know that the sum of two odd numbers is even. ↵ | This proves that the sum of two even numbers is always even. |
| sample | So, we know that 2 + 5 + 4 = 2 + 5. ↵  ↵ So, 3 + 6 + 2 + 5 = 6. ↵  ↵ Therefore, 2 + 5 = 3 + 6. ↵  ↵ From the above equation, we can see that 3 + 6 = 4 + 5. ↵  ↵ This proves that the sum of two odd numbers is always even. ↵  ↵ Similarly, 4 + 5 = 10. ↵  ↵ | This proves that the sum of two even numbers is always even. |
| sample | . ↵  ↵ The sum of any number is the opposite of the sum of integers. ↵  ↵ The sum of any number is always even. ↵  ↵ The following statements follow from the fact that: ↵  ↵ The sum of any number is even. ↵  ↵ The sum of any number is even on both sides of the sum. ↵  ↵ If we consider the case of the sum of two even numbers, we can see that: ↵  ↵ The sum of two even numbers is even. ↵  ↵ If the sum of two even numbers is even, it is even. ↵  ↵ | This proves that the sum of two even numbers is always even. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | An even number is any integer that can be divided by two without a remainder. | For example, 2 is even if 2 is divided by 2, 2 is even if 2 is divided by 2, and 2 is even if 2 is divided by 2. The number 2 is even if 2 is divided by 2, 2 is even if 2 is divided by 2, and 2 is even if 2 is divided by 2. The number 2 is even if 2 is divided |
| sample | An even number is any integer that can be divided by two without a remainder. | For example, 3^n has an even number of divisors (3, 6, 9) that can be divided by two without a remainder. It is even for integers such as n/2, 137, 28, 56, 98, 196, 242, 275, 311, 540, 1547, 2561, 3253, 3974, 53 |
| sample | An even number is any integer that can be divided by two without a remainder. | The term "even" is often used to denote negative numbers. It is used in many situations where dividing the number by two is not practical, but as a general rule, we use it to divide any number by a certain number without a remainder ↵  ↵ In mathematics, a number that can be divided by two without a remainder is called a divisor. The term "divisor" is often used to denote the number 3. The term "divisor" is |
| sample | An even number is any integer that can be divided by two without a remainder. | The number 100 is even if the decimal point is exactly ten. ↵ The number 100 is even if the decimal point is exactly 10. So, 100 can be divided by 2, 1, 2, 4, 8, 16, 20, 24, 32, 48, 64, 128, 80, 118, 101, 142, and 220 |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.767 | 47% |
| Backward | previous-token (right context) | 0.734 | 47% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `An` | 0.005 | 32 | `The` 0.06, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | An → ? | `␣even` | 0.000 | 367 | `alysis` 0.05, `atomy` 0.04, `␣Introduction` 0.03, `xiety` 0.03, `throp` 0.02 |
| 3 | An even → ? | `␣number` | 0.006 | 20 | `␣more` 0.32, `␣better` 0.15, `␣bigger` 0.07, `␣greater` 0.04, `␣simpler` 0.04 |
| 4 | An even number → ? | `␣is` | 0.060 | 2 | `␣of` 0.63, `␣is` 0.06, `,` 0.02, `␣can` 0.02, `␣` 0.02 |
| 5 | An even number is → ? | `␣any` | 0.005 | 23 | `␣` 0.18, `␣a` 0.11, `␣the` 0.10, `␣equal` 0.04, `␣one` 0.03 |
| 6 | …even number is any → ? | `␣integer` | 0.020 | 3 | `␣number` 0.65, `␣value` 0.02, `␣integer` 0.02, `␣positive` 0.02, `␣two` 0.02 |
| 7 | …number is any integer → ? | `␣that` | 0.184 | 1 | `␣that` 0.18, `␣greater` 0.13, `␣less` 0.10, `␣which` 0.06, `␣between` 0.05 |
| 8 | …is any integer that → ? | `␣can` | 0.113 | 2 | `␣is` 0.47, `␣can` 0.11, `␣has` 0.07, `␣divides` 0.05, `␣contains` 0.03 |
| 9 | …any integer that can → ? | `␣be` | 0.829 | 1 | `␣be` 0.83, `␣take` 0.02, `␣have` 0.01, `␣only` 0.01, `␣not` 0.01 |
| 10 | …integer that can be → ? | `␣divided` | 0.133 | 2 | `␣written` 0.21, `␣divided` 0.13, `␣expressed` 0.08, `␣represented` 0.07, `␣div` 0.03 |
| 11 | …that can be divided → ? | `␣by` | 0.760 | 1 | `␣by` 0.76, `␣into` 0.06, `␣evenly` 0.06, `␣up` 0.02, `␣equally` 0.02 |
| 12 | …can be divided by → ? | `␣two` | 0.045 | 6 | `␣` 0.23, `␣itself` 0.14, `␣a` 0.14, `␣the` 0.09, `␣any` 0.08 |
| 13 | …be divided by two → ? | `␣without` | 0.052 | 3 | `.` 0.21, `,` 0.12, `␣without` 0.05, `␣or` 0.05, `␣and` 0.04 |
| 14 | …divided by two without → ? | `␣a` | 0.089 | 1 | `␣a` 0.09, `␣any` 0.07, `␣leaving` 0.04, `␣the` 0.04, `␣losing` 0.04 |
| 15 | …by two without a → ? | `␣remainder` | 0.381 | 1 | `␣remainder` 0.38, `␣div` 0.06, `␣significant` 0.04, `␣leading` 0.04, `␣division` 0.03 |
| 16 | …two without a remainder → ? | `.` | 0.507 | 1 | `.` 0.51, `,` 0.11, `.\n` 0.07, `␣(` 0.04, `␣of` 0.03 |
| 17 | …without a remainder. → ? | `␣If` | 0.036 | 7 | `␣For` 0.16, `␣The` 0.12, `␣A` 0.07, `␣In` 0.06, `␣This` 0.05 |
| 18 | …a remainder. If → ? | `␣we` | 0.050 | 5 | `␣the` 0.17, `␣a` 0.15, `␣you` 0.12, `␣two` 0.07, `␣we` 0.05 |
| 19 | …remainder. If we → ? | `␣add` | 0.013 | 14 | `␣have` 0.16, `␣want` 0.12, `␣divide` 0.12, `␣are` 0.07, `␣know` 0.06 |
| 20 | …. If we add → ? | `␣two` | 0.256 | 1 | `␣two` 0.26, `␣` 0.18, `␣a` 0.12, `␣up` 0.11, `␣the` 0.07 |
| 21 | …If we add two → ? | `␣even` | 0.061 | 3 | `␣numbers` 0.33, `␣integers` 0.21, `␣even` 0.06, `␣` 0.06, `␣consecutive` 0.02 |
| 22 | …we add two even → ? | `␣numbers` | 0.851 | 1 | `␣numbers` 0.85, `␣integers` 0.10, `␣number` 0.01, `␣digits` 0.01, `␣whole` 0.00 |
| 23 | …add two even numbers → ? | `,` | 0.364 | 1 | `,` 0.36, `␣together` 0.36, `␣we` 0.04, `␣then` 0.03, `␣without` 0.02 |
| 24 | …two even numbers, → ? | `␣each` | 0.009 | 10 | `␣we` 0.41, `␣the` 0.18, `␣then` 0.10, `␣they` 0.04, `␣it` 0.03 |
| 25 | …even numbers, each → ? | `␣can` | 0.014 | 13 | `␣of` 0.17, `␣one` 0.14, `␣number` 0.10, `␣with` 0.06, `␣has` 0.05 |
| 26 | …numbers, each can → ? | `␣be` | 0.825 | 1 | `␣be` 0.82, `␣have` 0.03, `␣also` 0.02, `␣only` 0.02, `␣become` 0.01 |
| 27 | …, each can be → ? | `␣written` | 0.177 | 2 | `␣divided` 0.43, `␣written` 0.18, `␣added` 0.05, `␣multiplied` 0.04, `␣expressed` 0.03 |
| 28 | …each can be written → ? | `␣as` | 0.856 | 1 | `␣as` 0.86, `␣in` 0.07, `␣to` 0.01, `␣with` 0.01, `␣out` 0.01 |
| 29 | …can be written as → ? | `␣two` | 0.044 | 5 | `␣a` 0.35, `␣an` 0.13, `␣` 0.09, `␣the` 0.05, `␣two` 0.04 |
| 30 | …be written as two → ? | `␣times` | 0.030 | 7 | `␣even` 0.14, `␣` 0.10, `␣+` 0.09, `␣integers` 0.05, `␣add` 0.03 |
| 31 | …written as two times → ? | `␣some` | 0.000 | 109 | `␣the` 0.39, `␣two` 0.14, `␣` 0.09, `␣as` 0.05, `␣their` 0.04 |
| 32 | …as two times some → ? | `␣integer` | 0.186 | 1 | `␣integer` 0.19, `␣number` 0.15, `␣positive` 0.06, `␣other` 0.06, `␣even` 0.06 |
| 33 | …two times some integer → ? | `,` | 0.182 | 2 | `.` 0.19, `,` 0.18, `␣(` 0.05, `␣n` 0.04, `␣and` 0.03 |
| 34 | …times some integer, → ? | `␣so` | 0.038 | 5 | `␣and` 0.13, `␣such` 0.07, `␣which` 0.07, `␣or` 0.05, `␣so` 0.04 |
| 35 | …some integer, so → ? | `␣their` | 0.004 | 31 | `␣we` 0.21, `␣the` 0.20, `␣that` 0.06, `␣` 0.05, `␣for` 0.04 |
| 36 | …integer, so their → ? | `␣sum` | 0.219 | 1 | `␣sum` 0.22, `␣product` 0.18, `␣quot` 0.11, `␣remainder` 0.06, `␣div` 0.04 |
| 37 | …, so their sum → ? | `␣is` | 0.529 | 1 | `␣is` 0.53, `␣can` 0.12, `␣must` 0.09, `␣will` 0.08, `␣equals` 0.02 |
| 38 | …so their sum is → ? | `␣two` | 0.031 | 9 | `␣` 0.18, `␣equal` 0.10, `␣even` 0.09, `␣the` 0.07, `␣a` 0.07 |
| 39 | …their sum is two → ? | `␣times` | 0.467 | 1 | `␣times` 0.47, `.` 0.18, `.\n` 0.05, `␣even` 0.04, `,` 0.04 |
| 40 | …sum is two times → ? | `␣the` | 0.220 | 2 | `␣` 0.24, `␣the` 0.22, `␣two` 0.14, `␣their` 0.06, `␣some` 0.05 |
| 41 | …is two times the → ? | `␣sum` | 0.279 | 1 | `␣sum` 0.28, `␣number` 0.17, `␣integer` 0.08, `␣product` 0.07, `␣remainder` 0.04 |
| 42 | …two times the sum → ? | `␣of` | 0.973 | 1 | `␣of` 0.97, `.` 0.00, `␣(` 0.00, `,` 0.00, `␣for` 0.00 |
| 43 | …times the sum of → ? | `␣those` | 0.009 | 9 | `␣the` 0.50, `␣their` 0.28, `␣two` 0.05, `␣all` 0.02, `␣any` 0.02 |
| 44 | …the sum of those → ? | `␣integers` | 0.048 | 3 | `␣two` 0.58, `␣numbers` 0.14, `␣integers` 0.05, `␣div` 0.02, `␣parts` 0.02 |
| 45 | …sum of those integers → ? | `.` | 0.549 | 1 | `.` 0.55, `.\n` 0.13, `,` 0.09, `.\n\n` 0.06, `␣(` 0.02 |
| 46 | …of those integers. → ? | `␣This` | 0.071 | 4 | `␣For` 0.12, `␣The` 0.11, `␣If` 0.09, `␣This` 0.07, `␣In` 0.06 |
| 47 | …those integers. This → ? | `␣proves` | 0.001 | 95 | `␣is` 0.39, `␣means` 0.11, `␣can` 0.06, `␣number` 0.05, `␣sum` 0.03 |
| 48 | …integers. This proves → ? | `␣that` | 0.579 | 1 | `␣that` 0.58, `␣the` 0.11, `␣to` 0.07, `␣a` 0.02, `␣useful` 0.02 |
| 49 | …. This proves that → ? | `␣the` | 0.209 | 1 | `␣the` 0.21, `␣even` 0.09, `␣there` 0.07, `␣we` 0.06, `␣a` 0.05 |
| 50 | …This proves that the → ? | `␣sum` | 0.184 | 1 | `␣sum` 0.18, `␣number` 0.14, `␣even` 0.06, `␣two` 0.04, `␣integers` 0.04 |
| 51 | …proves that the sum → ? | `␣of` | 0.726 | 1 | `␣of` 0.73, `␣is` 0.18, `␣can` 0.02, `␣and` 0.01, `␣must` 0.01 |
| 52 | …that the sum of → ? | `␣two` | 0.327 | 1 | `␣two` 0.33, `␣the` 0.17, `␣any` 0.10, `␣even` 0.09, `␣a` 0.04 |
| 53 | …the sum of two → ? | `␣even` | 0.693 | 1 | `␣even` 0.69, `␣integers` 0.15, `␣numbers` 0.04, `␣odd` 0.02, `␣integer` 0.01 |
| 54 | …sum of two even → ? | `␣numbers` | 0.818 | 1 | `␣numbers` 0.82, `␣integers` 0.16, `␣number` 0.00, `␣integer` 0.00, `␣is` 0.00 |
| 55 | …of two even numbers → ? | `␣is` | 0.785 | 1 | `␣is` 0.79, `␣can` 0.08, `␣must` 0.02, `␣cannot` 0.02, `,` 0.01 |
| 56 | …two even numbers is → ? | `␣always` | 0.062 | 6 | `␣two` 0.19, `␣equal` 0.11, `␣` 0.07, `␣even` 0.07, `␣a` 0.07 |
| 57 | …even numbers is always → ? | `␣even` | 0.055 | 8 | `␣two` 0.25, `␣a` 0.10, `␣the` 0.09, `␣equal` 0.09, `␣greater` 0.07 |
| 58 | …numbers is always even → ? | `.` | 0.353 | 1 | `.` 0.35, `.\n` 0.25, `,` 0.14, `.\n\n` 0.09, `␣if` 0.02 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.519 | 1 | `.` 0.52, `!` 0.03, `)` 0.02, `).` 0.01, `?` 0.01 |
| 2 | ? ← . | `␣even` | 0.000 | 6599 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣Yes` 0.00, `␣years` 0.00 |
| 3 | ? ← even. | `␣always` | 0.004 | 25 | `␣and` 0.12, `␣is` 0.07, `␣or` 0.06, `␣more` 0.04, `␣not` 0.04 |
| 4 | ? ← always even. | `␣is` | 0.449 | 1 | `␣is` 0.45, `␣not` 0.19, `␣are` 0.13, `'s` 0.03, `␣was` 0.02 |
| 5 | ? ← is always even. | `␣numbers` | 0.004 | 28 | `␣it` 0.07, `␣It` 0.03, `␣that` 0.03, `)` 0.02, `␣which` 0.02 |
| 6 | ? ← numbers is always even… | `␣even` | 0.133 | 1 | `␣even` 0.13, `␣of` 0.13, `␣two` 0.11, `␣prime` 0.08, `␣odd` 0.07 |
| 7 | ? ← even numbers is always… | `␣two` | 0.143 | 2 | `␣of` 0.54, `␣two` 0.14, `␣for` 0.04, `␣all` 0.03, `␣with` 0.03 |
| 8 | ? ← two even numbers is… | `␣of` | 0.701 | 1 | `␣of` 0.70, `␣between` 0.11, `␣any` 0.04, `␣adding` 0.02, `␣multiplying` 0.01 |
| 9 | ? ← of two even numbers… | `␣sum` | 0.173 | 2 | `␣product` 0.53, `␣sum` 0.17, `␣difference` 0.03, `␣addition` 0.02, `␣ratio` 0.02 |
| 10 | ? ← sum of two even… | `␣the` | 0.605 | 1 | `␣the` 0.60, `␣The` 0.24, `␣a` 0.04, `The` 0.02, `␣that` 0.01 |
| 11 | ? ← the sum of two… | `␣that` | 0.339 | 1 | `␣that` 0.34, `,` 0.28, `␣of` 0.04, `␣and` 0.03, `␣if` 0.02 |
| 12 | ? ← that the sum of… | `␣proves` | 0.003 | 51 | `␣states` 0.15, `␣such` 0.06, `␣fact` 0.06, `␣is` 0.04, `␣so` 0.04 |
| 13 | ? ← proves that the sum… | `␣This` | 0.060 | 5 | `␣It` 0.18, `␣which` 0.08, `␣theorem` 0.07, `␣that` 0.06, `␣This` 0.06 |
| 14 | ? ← This proves that the… | `.` | 0.812 | 1 | `.` 0.81, `:` 0.05, `).` 0.03, `␣.` 0.01, `)` 0.01 |
| 15 | ? ← . This proves that… | `␣integers` | 0.004 | 26 | `␣even` 0.16, `␣odd` 0.05, `␣numbers` 0.05, `␣number` 0.04, `2` 0.04 |
| 16 | ? ← integers. This proves… | `␣those` | 0.001 | 47 | `␣even` 0.28, `␣two` 0.11, `␣are` 0.09, `␣odd` 0.07, `␣the` 0.07 |
| 17 | ? ← those integers. This… | `␣of` | 0.532 | 1 | `␣of` 0.53, `␣to` 0.04, `␣all` 0.04, `␣even` 0.03, `␣add` 0.03 |
| 18 | ? ← of those integers.… | `␣sum` | 0.374 | 1 | `␣sum` 0.37, `␣product` 0.06, `␣squares` 0.04, `␣one` 0.03, `␣ratio` 0.03 |
| 19 | ? ← sum of those integers… | `␣the` | 0.852 | 1 | `␣the` 0.85, `␣even` 0.04, `␣a` 0.01, `␣odd` 0.01, `␣total` 0.01 |
| 20 | ? ← the sum of those… | `␣times` | 0.005 | 22 | `␣is` 0.17, `␣of` 0.11, `␣to` 0.08, `␣as` 0.08, `␣be` 0.06 |
| 21 | ? ← times the sum of… | `␣two` | 0.043 | 6 | `␣number` 0.10, `␣integers` 0.07, `␣integer` 0.06, `␣numbers` 0.06, `2` 0.05 |
| 22 | ? ← two times the sum… | `␣is` | 0.448 | 1 | `␣is` 0.45, `␣be` 0.14, `␣to` 0.05, `␣equals` 0.03, `␣always` 0.03 |
| 23 | ? ← is two times the… | `␣sum` | 0.023 | 8 | `␣integers` 0.22, `␣numbers` 0.20, `␣number` 0.13, `␣integer` 0.04, `␣that` 0.03 |
| 24 | ? ← sum is two times… | `␣their` | 0.297 | 2 | `␣the` 0.42, `␣their` 0.30, `␣its` 0.06, `␣whose` 0.05, `␣The` 0.03 |
| 25 | ? ← their sum is two… | `␣so` | 0.042 | 5 | `,` 0.27, `␣that` 0.23, `␣then` 0.12, `␣and` 0.09, `␣so` 0.04 |
| 26 | ? ← so their sum is… | `,` | 0.643 | 1 | `,` 0.64, `␣and` 0.10, `␣even` 0.05, `␣integers` 0.04, `␣numbers` 0.02 |
| 27 | ? ← , so their sum… | `␣integer` | 0.042 | 4 | `␣even` 0.21, `␣integers` 0.19, `␣numbers` 0.07, `␣integer` 0.04, `␣equal` 0.04 |
| 28 | ? ← integer, so their… | `␣some` | 0.002 | 40 | `␣even` 0.27, `␣an` 0.12, `␣odd` 0.09, `␣positive` 0.04, `␣same` 0.04 |
| 29 | ? ← some integer, so… | `␣times` | 0.037 | 7 | `␣to` 0.20, `␣of` 0.16, `␣by` 0.08, `␣is` 0.06, `␣even` 0.04 |
| 30 | ? ← times some integer,… | `␣two` | 0.420 | 1 | `␣two` 0.42, `2` 0.09, `␣three` 0.05, `␣integer` 0.04, `␣integers` 0.03 |
| 31 | ? ← two times some integer… | `␣as` | 0.012 | 10 | `␣is` 0.49, `␣are` 0.08, `␣of` 0.07, `␣by` 0.05, `␣to` 0.03 |
| 32 | ? ← as two times some… | `␣written` | 0.242 | 1 | `␣written` 0.24, `␣same` 0.08, `␣expressed` 0.05, `␣counted` 0.04, `␣represented` 0.03 |
| 33 | ? ← written as two times… | `␣be` | 0.676 | 1 | `␣be` 0.68, `␣are` 0.17, `␣is` 0.06, `␣always` 0.01, `␣also` 0.01 |
| 34 | ? ← be written as two… | `␣can` | 0.768 | 1 | `␣can` 0.77, `␣also` 0.04, `␣cannot` 0.03, `␣must` 0.02, `␣may` 0.02 |
| 35 | ? ← can be written as… | `␣each` | 0.006 | 17 | `␣integers` 0.27, `␣numbers` 0.27, `␣integer` 0.08, `␣number` 0.05, `␣they` 0.02 |
| 36 | ? ← each can be written… | `,` | 0.223 | 1 | `,` 0.22, `␣of` 0.09, `␣that` 0.09, `␣and` 0.08, `␣numbers` 0.08 |
| 37 | ? ← , each can be… | `␣numbers` | 0.140 | 2 | `␣integers` 0.22, `␣numbers` 0.14, `␣integer` 0.06, `␣even` 0.05, `␣odd` 0.02 |
| 38 | ? ← numbers, each can… | `␣even` | 0.590 | 1 | `␣even` 0.59, `␣odd` 0.14, `␣two` 0.14, `␣Even` 0.03, `␣of` 0.01 |
| 39 | ? ← even numbers, each… | `␣two` | 0.687 | 1 | `␣two` 0.69, `␣Two` 0.07, `␣are` 0.06, `␣of` 0.04, `2` 0.03 |
| 40 | ? ← two even numbers,… | `␣add` | 0.021 | 7 | `␣of` 0.31, `␣have` 0.17, `␣are` 0.16, `␣any` 0.04, `,` 0.03 |
| 41 | ? ← add two even numbers… | `␣we` | 0.298 | 2 | `␣you` 0.51, `␣we` 0.30, `␣to` 0.12, `␣I` 0.01, `␣can` 0.01 |
| 42 | ? ← we add two even… | `␣If` | 0.295 | 1 | `␣If` 0.30, `␣if` 0.28, `If` 0.11, `␣when` 0.11, `␣When` 0.11 |
| 43 | ? ← If we add two… | `.` | 0.681 | 1 | `.` 0.68, `:` 0.16, `?` 0.02, `,` 0.01, `)` 0.01 |
| 44 | ? ← . If we add… | `␣remainder` | 0.002 | 48 | `␣even` 0.15, `␣integers` 0.12, `␣numbers` 0.10, `␣odd` 0.06, `␣integer` 0.04 |
| 45 | ? ← remainder. If we… | `␣a` | 0.159 | 3 | `␣no` 0.32, `␣the` 0.27, `␣a` 0.16, `␣any` 0.03, `␣zero` 0.03 |
| 46 | ? ← a remainder. If… | `␣without` | 0.083 | 5 | `␣leaving` 0.13, `␣leave` 0.12, `␣leaves` 0.12, `␣have` 0.09, `␣without` 0.08 |
| 47 | ? ← without a remainder.… | `␣two` | 0.010 | 14 | `␣even` 0.13, `␣integers` 0.11, `,` 0.09, `␣numbers` 0.06, `␣number` 0.06 |
| 48 | ? ← two without a remainder… | `␣by` | 0.425 | 1 | `␣by` 0.43, `␣of` 0.14, `␣into` 0.09, `␣times` 0.07, `␣add` 0.04 |
| 49 | ? ← by two without a… | `␣divided` | 0.150 | 2 | `isible` 0.40, `␣divided` 0.15, `␣two` 0.09, `␣divide` 0.08, `␣number` 0.05 |
| 50 | ? ← divided by two without… | `␣be` | 0.901 | 1 | `␣be` 0.90, `␣is` 0.02, `␣number` 0.01, `␣when` 0.01, `␣being` 0.00 |
| 51 | ? ← be divided by two… | `␣can` | 0.698 | 1 | `␣can` 0.70, `␣cannot` 0.18, `␣always` 0.02, `'t` 0.01, `␣may` 0.01 |
| 52 | ? ← can be divided by… | `␣that` | 0.190 | 1 | `␣that` 0.19, `␣numbers` 0.18, `␣number` 0.13, `␣integer` 0.08, `␣integers` 0.06 |
| 53 | ? ← that can be divided… | `␣integer` | 0.109 | 3 | `␣number` 0.46, `␣numbers` 0.22, `␣integer` 0.11, `␣integers` 0.08, `␣one` 0.02 |
| 54 | ? ← integer that can be… | `␣any` | 0.071 | 5 | `␣an` 0.18, `␣smallest` 0.17, `␣largest` 0.10, `␣positive` 0.07, `␣any` 0.07 |
| 55 | ? ← any integer that can… | `␣is` | 0.675 | 1 | `␣is` 0.67, `␣be` 0.07, `␣as` 0.06, `␣of` 0.03, `␣to` 0.02 |
| 56 | ? ← is any integer that… | `␣number` | 0.320 | 2 | `␣integer` 0.51, `␣number` 0.32, `␣integers` 0.02, `␣even` 0.01, `␣sum` 0.01 |
| 57 | ? ← number is any integer… | `␣even` | 0.892 | 1 | `␣even` 0.89, `␣odd` 0.07, `␣prime` 0.00, `␣Even` 0.00, `␣rational` 0.00 |
| 58 | ? ← even number is any… | `An` | 0.401 | 2 | `␣An` 0.45, `An` 0.40, `␣an` 0.13, `,` 0.00, `␣or` 0.00 |

---

## 9. water_boils

*Category: logical*

> **Beginning:** Water boils when its vapour pressure equals the pressure of the surrounding air.  
> **Middle:** At high altitude the air pressure is lower, so less heat is needed to reach that point.  
> **Ending:** That is why water boils at a lower temperature on top of a mountain.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | where the temperature is higher than the boiling point of water, it will continue to heat up to a point where the temperature is higher than the boiling point of water, it will continue to heat up to a point where the temperature is higher than the boiling point of water, it will continue to heat up to a point where the temperature is higher than the boiling point of water, it will continue to heat up to a point where the temperature is higher than the boiling point of water. ↵ | That is why water boils at a lower temperature on top of a mountain. |
| sample | of water change with temperature? ↵ As the temperature increases, the pressure difference at the boiling points increases, which lowers the boiling point of water. This is because it has a larger amount of intermolecular force, which increases the temperature of boiling water. ↵ What affects the temperature where water boils? ↵ The boiling point of water is affected by changes in temperature. When water gets colder, the molecules can freeze and increase in size. This increase in volume ends up being able to hold more water. ↵ | That is why water boils at a lower temperature on top of a mountain. |
| sample | cooler than the air temperature on Earth. ↵  ↵ The boiling point is dependent on the temperature of the air. Scientists believe that heat is released when air is heated above the boiling point of water by the distillation of air. ↵  ↵ On the Earth's surface and on mountains and mountains, air is compressed. As the air expands, it continues to expand. At low temperatures, it freezes. But when it is subjected to high temperatures, it boils. The heat released increases, and the temperature rises. ↵  ↵ | That is why water boils at a lower temperature on top of a mountain. |
| sample | to boil, and the water boils at the boiling point. ↵  ↵ Salt usually boils at the boiling point, because salt has a lower boiling point than water. ↵  ↵ In general, fresh water has a lower boiling point than water at sea level, as the water rises in temperature away from the boiling point. ↵  ↵ At sea level, there is very little heat, and the atmosphere is not surrounded by water. ↵  ↵ At sea level, there is a lot of heat, and the atmosphere is surrounded by water. ↵  ↵ | That is why water boils at a lower temperature on top of a mountain. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | Water boils when its vapour pressure equals the pressure of the surrounding air. | The boiling point of water is 100°C. The boiling point of water is 100°C. The boiling point of water is 100°C. The boiling point of water is 100°C. The boiling point of water is 100°C. The boiling point of water is 100°C. The boiling point of water is 100°C. The boiling point of water is 100°C. The boiling point of water is 10 |
| sample | Water boils when its vapour pressure equals the pressure of the surrounding air. | The boiling point of a liquid or gas is the temperature at which the vapour pressure of that liquid or gas changes from the vapour pressure of the surrounding liquid or gas to the vapour pressure of the liquid or gas. ↵ Can water boil on its own? ↵ Boiling water is a chemical reaction that occurs when heat is applied to a liquid. The pressure that the liquid exerts on the surface of the liquid changes. When this pressure equals the pressure of the surrounding air pressure, the liquid rises |
| sample | Water boils when its vapour pressure equals the pressure of the surrounding air. | This effect is called boiling point elevation. ↵ Boiling point elevation occurs when water molecules in contact with a solvent are converted to a gas, and at that point the vapor pressure of the liquid is equal to the pressure of the solvent. In water, as it boils, the vapor pressure is equal to the pressure of the surrounding air. The boiling point of water is 100 degrees C. when the air is at a pressure of 1 atmosphere, the water molecules are converted to |
| sample | Water boils when its vapour pressure equals the pressure of the surrounding air. | This is generally 100% evaporation. At the boiling point of water, the pressure of the surrounding air is equal to the pressure of the water. In other words, the water boils at that pressure. That is, water's vapour pressure equals its own pressure, and it boils at 100% (100% is the vapour pressure of water at sea level). ↵ What is the boiling point of an ice cube? ↵ The boiling point of water is the temperature at which |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.625 | 46% |
| Backward | previous-token (right context) | 0.658 | 44% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `Water` | 0.001 | 186 | `The` 0.06, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | Water → ? | `␣boils` | 0.000 | 294 | `␣is` 0.07, `color` 0.03, `melon` 0.02, `␣Quality` 0.02, `␣quality` 0.02 |
| 3 | Water boils → ? | `␣when` | 0.040 | 2 | `␣at` 0.68, `␣when` 0.04, `␣faster` 0.03, `␣in` 0.02, `,` 0.02 |
| 4 | Water boils when → ? | `␣its` | 0.103 | 3 | `␣the` 0.33, `␣it` 0.18, `␣its` 0.10, `␣temperature` 0.06, `␣` 0.04 |
| 5 | Water boils when its → ? | `␣vapour` | 0.018 | 6 | `␣temperature` 0.55, `␣vapor` 0.16, `␣molecules` 0.04, `␣specific` 0.03, `␣density` 0.02 |
| 6 | …boils when its vapour → ? | `␣pressure` | 0.863 | 1 | `␣pressure` 0.86, `␣is` 0.02, `␣content` 0.01, `␣temperature` 0.01, `␣turns` 0.01 |
| 7 | …when its vapour pressure → ? | `␣equals` | 0.056 | 6 | `␣is` 0.44, `␣decreases` 0.08, `␣reaches` 0.07, `␣exceeds` 0.06, `␣increases` 0.06 |
| 8 | …its vapour pressure equals → ? | `␣the` | 0.420 | 1 | `␣the` 0.42, `␣its` 0.19, `␣that` 0.13, `␣` 0.08, `␣atmospheric` 0.07 |
| 9 | …vapour pressure equals the → ? | `␣pressure` | 0.083 | 2 | `␣atmospheric` 0.43, `␣pressure` 0.08, `␣saturation` 0.06, `␣vapour` 0.04, `␣surrounding` 0.04 |
| 10 | …pressure equals the pressure → ? | `␣of` | 0.616 | 1 | `␣of` 0.62, `␣at` 0.18, `␣in` 0.04, `␣inside` 0.03, `␣exerted` 0.02 |
| 11 | …equals the pressure of → ? | `␣the` | 0.656 | 1 | `␣the` 0.66, `␣its` 0.16, `␣a` 0.02, `␣atmospheric` 0.02, `␣water` 0.01 |
| 12 | …the pressure of the → ? | `␣surrounding` | 0.282 | 1 | `␣surrounding` 0.28, `␣liquid` 0.23, `␣gas` 0.11, `␣atmosphere` 0.06, `␣surroundings` 0.05 |
| 13 | …pressure of the surrounding → ? | `␣air` | 0.289 | 1 | `␣air` 0.29, `␣atmosphere` 0.21, `␣liquid` 0.14, `␣gas` 0.09, `␣environment` 0.05 |
| 14 | …of the surrounding air → ? | `.` | 0.411 | 1 | `.` 0.41, `␣at` 0.23, `,` 0.10, `.\n` 0.04, `␣(` 0.04 |
| 15 | …the surrounding air. → ? | `␣At` | 0.023 | 10 | `␣The` 0.16, `␣This` 0.12, `␣If` 0.05, `␣When` 0.05, `␣Water` 0.05 |
| 16 | …surrounding air. At → ? | `␣high` | 0.051 | 7 | `␣the` 0.13, `␣a` 0.12, `␣` 0.09, `␣sea` 0.07, `␣this` 0.07 |
| 17 | …air. At high → ? | `␣altitude` | 0.065 | 6 | `␣altitudes` 0.28, `␣temperatures` 0.21, `␣pressure` 0.16, `␣temperature` 0.11, `␣pressures` 0.07 |
| 18 | …. At high altitude → ? | `␣the` | 0.168 | 2 | `,` 0.55, `␣the` 0.17, `␣water` 0.04, `␣this` 0.03, `␣it` 0.02 |
| 19 | …At high altitude the → ? | `␣air` | 0.229 | 1 | `␣air` 0.23, `␣pressure` 0.13, `␣vapour` 0.12, `␣boiling` 0.10, `␣water` 0.06 |
| 20 | …high altitude the air → ? | `␣pressure` | 0.357 | 1 | `␣pressure` 0.36, `␣is` 0.26, `␣becomes` 0.06, `␣has` 0.03, `␣around` 0.02 |
| 21 | …altitude the air pressure → ? | `␣is` | 0.614 | 1 | `␣is` 0.61, `␣decreases` 0.05, `␣becomes` 0.05, `␣increases` 0.04, `␣drops` 0.03 |
| 22 | …the air pressure is → ? | `␣lower` | 0.129 | 1 | `␣lower` 0.13, `␣less` 0.09, `␣much` 0.09, `␣reduced` 0.08, `␣low` 0.07 |
| 23 | …air pressure is lower → ? | `,` | 0.225 | 2 | `␣than` 0.25, `,` 0.22, `␣and` 0.20, `.` 0.08, `␣so` 0.05 |
| 24 | …pressure is lower, → ? | `␣so` | 0.302 | 1 | `␣so` 0.30, `␣and` 0.19, `␣the` 0.07, `␣but` 0.06, `␣which` 0.05 |
| 25 | …is lower, so → ? | `␣less` | 0.023 | 8 | `␣the` 0.37, `␣water` 0.18, `␣there` 0.05, `␣it` 0.05, `␣that` 0.05 |
| 26 | …lower, so less → ? | `␣heat` | 0.025 | 5 | `␣water` 0.41, `␣vapour` 0.34, `␣boiling` 0.04, `␣of` 0.03, `␣heat` 0.02 |
| 27 | …, so less heat → ? | `␣is` | 0.831 | 1 | `␣is` 0.83, `␣energy` 0.06, `␣can` 0.02, `␣escapes` 0.02, `␣will` 0.01 |
| 28 | …so less heat is → ? | `␣needed` | 0.060 | 6 | `␣generated` 0.21, `␣required` 0.17, `␣produced` 0.10, `␣absorbed` 0.08, `␣lost` 0.07 |
| 29 | …less heat is needed → ? | `␣to` | 0.882 | 1 | `␣to` 0.88, `␣for` 0.06, `.` 0.02, `,` 0.01, `.\n` 0.00 |
| 30 | …heat is needed to → ? | `␣reach` | 0.006 | 25 | `␣boil` 0.23, `␣raise` 0.23, `␣evaporate` 0.05, `␣increase` 0.04, `␣overcome` 0.03 |
| 31 | …is needed to reach → ? | `␣that` | 0.008 | 8 | `␣the` 0.63, `␣a` 0.11, `␣boiling` 0.08, `␣it` 0.03, `␣water` 0.01 |
| 32 | …needed to reach that → ? | `␣point` | 0.104 | 4 | `␣temperature` 0.25, `␣boiling` 0.20, `␣altitude` 0.14, `␣point` 0.10, `␣level` 0.05 |
| 33 | …to reach that point → ? | `.` | 0.625 | 1 | `.` 0.63, `.\n` 0.10, `,` 0.09, `.\n\n` 0.03, `␣of` 0.02 |
| 34 | …reach that point. → ? | `␣That` | 0.009 | 20 | `␣The` 0.12, `␣At` 0.11, `␣This` 0.09, `␣As` 0.06, `␣However` 0.04 |
| 35 | …that point. That → ? | `␣is` | 0.282 | 2 | `'s` 0.29, `␣is` 0.28, `␣means` 0.15, `␣heat` 0.03, `␣makes` 0.02 |
| 36 | …point. That is → ? | `␣why` | 0.691 | 1 | `␣why` 0.69, `,` 0.10, `␣the` 0.08, `␣because` 0.02, `␣what` 0.01 |
| 37 | …. That is why → ? | `␣water` | 0.112 | 2 | `␣the` 0.16, `␣water` 0.11, `␣you` 0.07, `␣it` 0.05, `␣a` 0.04 |
| 38 | …That is why water → ? | `␣boils` | 0.561 | 1 | `␣boils` 0.56, `␣is` 0.05, `␣freezes` 0.05, `␣boiling` 0.03, `␣can` 0.02 |
| 39 | …is why water boils → ? | `␣at` | 0.581 | 1 | `␣at` 0.58, `␣when` 0.13, `␣in` 0.03, `.` 0.03, `␣faster` 0.02 |
| 40 | …why water boils at → ? | `␣a` | 0.148 | 2 | `␣` 0.23, `␣a` 0.15, `␣high` 0.10, `␣sea` 0.10, `␣higher` 0.07 |
| 41 | …water boils at a → ? | `␣lower` | 0.380 | 1 | `␣lower` 0.38, `␣higher` 0.32, `␣temperature` 0.07, `␣high` 0.06, `␣much` 0.02 |
| 42 | …boils at a lower → ? | `␣temperature` | 0.826 | 1 | `␣temperature` 0.83, `␣altitude` 0.07, `␣boiling` 0.04, `␣pressure` 0.01, `␣temp` 0.01 |
| 43 | …at a lower temperature → ? | `␣on` | 0.023 | 8 | `␣than` 0.32, `␣at` 0.24, `.` 0.08, `␣when` 0.06, `␣in` 0.04 |
| 44 | …a lower temperature on → ? | `␣top` | 0.007 | 18 | `␣the` 0.27, `␣a` 0.26, `␣high` 0.10, `␣higher` 0.05, `␣mountains` 0.04 |
| 45 | …lower temperature on top → ? | `␣of` | 0.935 | 1 | `␣of` 0.93, `␣than` 0.02, `.` 0.01, `,` 0.01, `.\n` 0.01 |
| 46 | …temperature on top of → ? | `␣a` | 0.307 | 2 | `␣the` 0.33, `␣a` 0.31, `␣mountains` 0.03, `␣an` 0.03, `␣its` 0.02 |
| 47 | …on top of a → ? | `␣mountain` | 0.366 | 1 | `␣mountain` 0.37, `␣hill` 0.14, `␣cloud` 0.05, `␣higher` 0.05, `␣high` 0.04 |
| 48 | …top of a mountain → ? | `.` | 0.206 | 2 | `␣than` 0.23, `.` 0.21, `,` 0.14, `.\n` 0.13, `␣or` 0.05 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.519 | 1 | `.` 0.52, `!` 0.03, `)` 0.02, `).` 0.01, `?` 0.01 |
| 2 | ? ← . | `␣mountain` | 0.000 | 4336 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣Yes` 0.00, `␣years` 0.00 |
| 3 | ? ← mountain. | `␣a` | 0.169 | 2 | `␣the` 0.50, `␣a` 0.17, `␣or` 0.01, `␣this` 0.01, `␣your` 0.01 |
| 4 | ? ← a mountain. | `␣of` | 0.250 | 1 | `␣of` 0.25, `␣on` 0.14, `␣up` 0.06, `␣climbing` 0.05, `␣down` 0.05 |
| 5 | ? ← of a mountain. | `␣top` | 0.276 | 1 | `␣top` 0.28, `␣side` 0.12, `␣base` 0.07, `␣summit` 0.06, `␣peak` 0.03 |
| 6 | ? ← top of a mountain… | `␣on` | 0.298 | 2 | `␣the` 0.67, `␣on` 0.30, `␣The` 0.01, `␣very` 0.01, `␣or` 0.00 |
| 7 | ? ← on top of a… | `␣temperature` | 0.000 | 1264 | `␣or` 0.05, `␣sitting` 0.03, `␣standing` 0.02, `,` 0.02, `␣up` 0.02 |
| 8 | ? ← temperature on top of… | `␣lower` | 0.004 | 32 | `␣the` 0.15, `␣air` 0.11, `␣in` 0.09, `␣high` 0.03, `␣water` 0.03 |
| 9 | ? ← lower temperature on top… | `␣a` | 0.588 | 1 | `␣a` 0.59, `␣the` 0.10, `␣much` 0.05, `␣of` 0.04, `␣and` 0.04 |
| 10 | ? ← a lower temperature on… | `␣at` | 0.496 | 1 | `␣at` 0.50, `␣to` 0.15, `␣and` 0.11, `␣with` 0.03, `␣maintain` 0.02 |
| 11 | ? ← at a lower temperature… | `␣boils` | 0.022 | 5 | `␣is` 0.07, `␣water` 0.04, `␣and` 0.03, `␣air` 0.03, `␣boils` 0.02 |
| 12 | ? ← boils at a lower… | `␣water` | 0.499 | 1 | `␣water` 0.50, `␣Water` 0.14, `␣and` 0.05, `␣it` 0.04, `␣liquid` 0.03 |
| 13 | ? ← water boils at a… | `␣why` | 0.061 | 5 | `,` 0.14, `␣that` 0.13, `␣when` 0.10, `␣where` 0.08, `␣why` 0.06 |
| 14 | ? ← why water boils at… | `␣is` | 0.287 | 1 | `␣is` 0.29, `␣explains` 0.13, `␣explain` 0.12, `'s` 0.07, `␣and` 0.05 |
| 15 | ? ← is why water boils… | `␣That` | 0.105 | 3 | `␣This` 0.38, `␣which` 0.32, `␣That` 0.10, `␣that` 0.05, `␣this` 0.05 |
| 16 | ? ← That is why water… | `.` | 0.924 | 1 | `.` 0.92, `).` 0.02, `␣…` 0.01, `:` 0.01, `?` 0.01 |
| 17 | ? ← . That is why… | `␣point` | 0.022 | 5 | `␣water` 0.06, `␣temperature` 0.05, `␣pressure` 0.04, `␣heat` 0.03, `␣point` 0.02 |
| 18 | ? ← point. That is… | `␣that` | 0.026 | 5 | `␣boiling` 0.62, `␣freezing` 0.14, `␣melting` 0.04, `␣triple` 0.03, `␣that` 0.03 |
| 19 | ? ← that point. That… | `␣reach` | 0.008 | 8 | `␣at` 0.74, `␣to` 0.07, `␣above` 0.04, `␣below` 0.03, `␣from` 0.03 |
| 20 | ? ← reach that point.… | `␣to` | 0.647 | 1 | `␣to` 0.65, `␣they` 0.08, `␣will` 0.05, `␣not` 0.04, `␣never` 0.03 |
| 21 | ? ← to reach that point… | `␣needed` | 0.022 | 10 | `␣energy` 0.10, `␣longer` 0.06, `␣water` 0.05, `␣heat` 0.05, `␣order` 0.04 |
| 22 | ? ← needed to reach that… | `␣is` | 0.544 | 1 | `␣is` 0.54, `␣energy` 0.12, `␣heat` 0.07, `␣be` 0.05, `␣are` 0.03 |
| 23 | ? ← is needed to reach… | `␣heat` | 0.215 | 2 | `␣energy` 0.35, `␣heat` 0.22, `␣that` 0.05, `␣pressure` 0.04, `␣water` 0.04 |
| 24 | ? ← heat is needed to… | `␣less` | 0.126 | 3 | `␣more` 0.56, `␣More` 0.14, `␣less` 0.13, `␣of` 0.05, `␣much` 0.03 |
| 25 | ? ← less heat is needed… | `␣so` | 0.158 | 3 | `,` 0.19, `␣the` 0.19, `␣so` 0.16, `␣and` 0.10, `␣because` 0.07 |
| 26 | ? ← so less heat is… | `,` | 0.685 | 1 | `,` 0.69, `␣and` 0.08, `␣point` 0.02, `␣temperature` 0.01, `),` 0.01 |
| 27 | ? ← , so less heat… | `␣lower` | 0.019 | 7 | `␣point` 0.15, `␣temperature` 0.08, `␣water` 0.04, `␣pressure` 0.03, `␣mountain` 0.03 |
| 28 | ? ← lower, so less… | `␣is` | 0.751 | 1 | `␣is` 0.75, `␣be` 0.05, `␣are` 0.04, `␣gets` 0.02, `␣much` 0.02 |
| 29 | ? ← is lower, so… | `␣pressure` | 0.092 | 3 | `␣temperature` 0.26, `␣point` 0.24, `␣pressure` 0.09, `␣mountain` 0.07, `␣water` 0.05 |
| 30 | ? ← pressure is lower,… | `␣air` | 0.084 | 3 | `␣the` 0.51, `␣atmospheric` 0.10, `␣air` 0.08, `␣vapor` 0.08, `␣The` 0.04 |
| 31 | ? ← air pressure is lower… | `␣the` | 0.617 | 1 | `␣the` 0.62, `,` 0.12, `␣The` 0.07, `␣because` 0.03, `␣and` 0.02 |
| 32 | ? ← the air pressure is… | `␣altitude` | 0.014 | 7 | `,` 0.39, `␣where` 0.16, `␣because` 0.14, `␣and` 0.05, `␣mountain` 0.03 |
| 33 | ? ← altitude the air pressure… | `␣high` | 0.173 | 2 | `␣higher` 0.47, `␣high` 0.17, `␣At` 0.07, `␣lower` 0.05, `At` 0.04 |
| 34 | ? ← high altitude the air… | `␣At` | 0.299 | 1 | `␣At` 0.30, `␣at` 0.26, `␣a` 0.24, `At` 0.13, `␣the` 0.02 |
| 35 | ? ← At high altitude the… | `.` | 0.892 | 1 | `.` 0.89, `).` 0.02, `:` 0.02, `?` 0.02, `-` 0.01 |
| 36 | ? ← . At high altitude… | `␣air` | 0.032 | 6 | `␣pressure` 0.16, `␣point` 0.09, `␣altitude` 0.09, `␣temperature` 0.05, `␣mountain` 0.04 |
| 37 | ? ← air. At high… | `␣surrounding` | 0.045 | 4 | `␣the` 0.52, `␣of` 0.08, `␣than` 0.05, `␣surrounding` 0.05, `␣cold` 0.04 |
| 38 | ? ← surrounding air. At… | `␣the` | 0.916 | 1 | `␣the` 0.92, `␣of` 0.02, `␣than` 0.01, `␣and` 0.01, `␣to` 0.01 |
| 39 | ? ← the surrounding air.… | `␣of` | 0.279 | 1 | `␣of` 0.28, `␣than` 0.23, `␣to` 0.13, `␣by` 0.06, `␣with` 0.05 |
| 40 | ? ← of the surrounding air… | `␣pressure` | 0.503 | 1 | `␣pressure` 0.50, `␣temperature` 0.26, `␣that` 0.11, `␣density` 0.04, `␣point` 0.01 |
| 41 | ? ← pressure of the surrounding… | `␣the` | 0.840 | 1 | `␣the` 0.84, `␣and` 0.03, `␣lower` 0.02, `␣vapor` 0.01, `␣air` 0.01 |
| 42 | ? ← the pressure of the… | `␣equals` | 0.011 | 14 | `␣to` 0.20, `␣by` 0.15, `␣and` 0.10, `␣on` 0.09, `␣than` 0.08 |
| 43 | ? ← equals the pressure of… | `␣pressure` | 0.374 | 1 | `␣pressure` 0.37, `␣it` 0.07, `␣air` 0.06, `␣point` 0.02, `␣water` 0.02 |
| 44 | ? ← pressure equals the pressure… | `␣vapour` | 0.011 | 12 | `␣air` 0.27, `␣the` 0.18, `␣vapor` 0.10, `␣its` 0.08, `␣that` 0.05 |
| 45 | ? ← vapour pressure equals the… | `␣its` | 0.242 | 2 | `␣the` 0.45, `␣its` 0.24, `␣water` 0.09, `␣saturated` 0.03, `␣in` 0.03 |
| 46 | ? ← its vapour pressure equals… | `␣when` | 0.192 | 2 | `␣until` 0.32, `␣when` 0.19, `␣where` 0.15, `␣that` 0.08, `,` 0.06 |
| 47 | ? ← when its vapour pressure… | `␣boils` | 0.145 | 2 | `␣point` 0.28, `␣boils` 0.14, `␣temperature` 0.08, `␣liquid` 0.06, `␣state` 0.04 |
| 48 | ? ← boils when its vapour… | `Water` | 0.293 | 1 | `Water` 0.29, `␣water` 0.27, `␣Water` 0.16, `␣liquid` 0.09, `␣only` 0.03 |

---

## 10. detective

*Category: logical*

> **Beginning:** The window had been forced open from the outside, and there was mud on the carpet.  
> **Middle:** The gardener was the only person with muddy boots, and he had been seen near the house at midnight.  
> **Ending:** The detective concluded that the gardener had broken into the study.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | what is happening in the garden,” he said. ↵ Part of the reason that gardeners are not aware of what is happening in the garden is because they are not aware of what is happening in the garden, he said. ↵ “The problem is that we are not aware of what is happening in the garden,” he said. ↵ “Now that we are aware of what is happening in the garden, we know that there is a problem, and we need to do something about it,” he said. ↵ | The detective concluded that the gardener had broken into the study. |
| sample | the garden.” ↵ John Brady, who has been working in the gardens in the area, visited the garden that day. ↵ “This is a great opportunity to talk about different things in our garden,” he said. ↵ “It is a great opportunity to meet other gardeners and how they relate to their work and to look at the different kinds of activity in their garden,” he said. ↵ “I will listen to them if they understand the impact that gardeners have on the garden,” he said. ↵ | The detective concluded that the gardener had broken into the study. |
| sample | the front of the house. ↵  ↵ Later, she ran out of the house, yelling that she was about to be run off by her dog. Eventually, the dog grabbed her arm and went to the front of the house. ↵  ↵ "Over there! I see you," she shouted. Eventually, her dog ran out of the house, grabbed her, and landed on her arm. The dog landed on her arm and ran off, but the gardener chose not to pick her up. ↵  ↵ | The detective concluded that the gardener had broken into the study. |
| sample | ahan said this has resulted in many gardens that have been hit hard by the drought. She said gardeners need to do what is best for the plants. ↵  ↵ "We have hard water, and water that doesn't go all the way down, that ↵ that gardener has to do something that helps hold the soil down. If it's down in the soil, and ↵ there's nothing to hold it down, there's nothing stopping the water from going in and out," ↵ he said. ↵  ↵ | The detective concluded that the gardener had broken into the study. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | The window had been forced open from the outside, and there was mud on the carpet. | The window was covered with a thick layer of mud, and the window was covered with a thick layer of mud. The window was covered with mud, and the window was covered with mud. The window was covered with mud, and the window was covered with mud. The window was covered with mud, and the window was covered with mud. The window was covered with mud, and the window was covered with mud. The window was covered with mud, and the window was covered with |
| sample | The window had been forced open from the outside, and there was mud on the carpet. | The window was now open, but the dampness was still there. She took a seat on the bed and began to open the door. She was surprised at how far the mud had stuck to her window. ↵ "What's wrong with you window?" She asked. ↵ "Don't you have a window, Mister?" Mister asked. ↵ "Well, I have a window that's been forced open by mud." ↵ The window had been forced open by mud for 3 years. No |
| sample | The window had been forced open from the outside, and there was mud on the carpet. | And all the windows in the room were covered by two sets of doors, the one at the front and one at the back. And there were three beds in the room, two at the front and one at the back, but there was little sign of the doors. And there were two sets of windows in the room, the one at the front and one at the back. ↵ And the place where the doors were opened was not the place where the windows were opened. And in |
| sample | The window had been forced open from the outside, and there was mud on the carpet. | It was all too warm. The person who could not get inside could not get out of the house. The window had been forced open from the outside. There was mud on the carpet. It was all too warm. The person who could not get inside could not get out of the house. The window had been forced open from the outside, and there was mud on the carpet. It was all too warm. The person who could not get inside could not get out of the |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 1.028 | 44% |
| Backward | previous-token (right context) | 1.085 | 37% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `The` | 0.057 | 1 | `The` 0.06, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | The → ? | `␣window` | 0.000 | 2116 | `␣` 0.02, `␣first` 0.01, `␣Importance` 0.01, `␣most` 0.01, `␣best` 0.01 |
| 3 | The window → ? | `␣had` | 0.001 | 174 | `␣is` 0.11, `␣of` 0.07, `less` 0.03, `␣s` 0.02, `␣frame` 0.02 |
| 4 | The window had → ? | `␣been` | 0.283 | 1 | `␣been` 0.28, `␣a` 0.15, `␣to` 0.03, `␣already` 0.03, `␣just` 0.03 |
| 5 | The window had been → ? | `␣forced` | 0.000 | 288 | `␣open` 0.09, `␣opened` 0.08, `␣closed` 0.07, `␣a` 0.03, `␣shut` 0.02 |
| 6 | …window had been forced → ? | `␣open` | 0.257 | 1 | `␣open` 0.26, `␣shut` 0.18, `␣down` 0.11, `␣to` 0.09, `␣closed` 0.07 |
| 7 | …had been forced open → ? | `␣from` | 0.006 | 20 | `␣by` 0.20, `,` 0.18, `␣and` 0.09, `␣with` 0.06, `␣for` 0.05 |
| 8 | …been forced open from → ? | `␣the` | 0.459 | 1 | `␣the` 0.46, `␣a` 0.08, `␣` 0.03, `␣inside` 0.02, `␣time` 0.02 |
| 9 | …forced open from the → ? | `␣outside` | 0.104 | 1 | `␣outside` 0.10, `␣inside` 0.07, `␣top` 0.04, `␣front` 0.03, `␣bottom` 0.03 |
| 10 | …open from the outside → ? | `,` | 0.281 | 1 | `,` 0.28, `.` 0.11, `␣by` 0.09, `␣and` 0.07, `␣in` 0.07 |
| 11 | …from the outside, → ? | `␣and` | 0.276 | 1 | `␣and` 0.28, `␣but` 0.13, `␣so` 0.07, `␣the` 0.05, `␣with` 0.04 |
| 12 | …the outside, and → ? | `␣there` | 0.034 | 5 | `␣the` 0.33, `␣it` 0.06, `␣a` 0.05, `␣I` 0.04, `␣there` 0.03 |
| 13 | …outside, and there → ? | `␣was` | 0.636 | 1 | `␣was` 0.64, `␣were` 0.22, `␣had` 0.05, `␣seemed` 0.01, `␣would` 0.01 |
| 14 | …, and there was → ? | `␣mud` | 0.000 | 282 | `␣no` 0.27, `␣a` 0.26, `␣nothing` 0.05, `␣still` 0.04, `␣an` 0.03 |
| 15 | …and there was mud → ? | `␣on` | 0.194 | 1 | `␣on` 0.19, `␣everywhere` 0.09, `␣all` 0.09, `␣and` 0.07, `␣in` 0.06 |
| 16 | …there was mud on → ? | `␣the` | 0.861 | 1 | `␣the` 0.86, `␣top` 0.03, `␣it` 0.02, `␣its` 0.02, `␣his` 0.01 |
| 17 | …was mud on the → ? | `␣carpet` | 0.002 | 36 | `␣floor` 0.15, `␣inside` 0.10, `␣window` 0.08, `␣wall` 0.07, `␣walls` 0.07 |
| 18 | …mud on the carpet → ? | `.` | 0.319 | 1 | `.` 0.32, `,` 0.17, `␣and` 0.06, `␣in` 0.03, `␣below` 0.03 |
| 19 | …on the carpet. → ? | `␣The` | 0.200 | 1 | `␣The` 0.20, `␣It` 0.06, `␣I` 0.05, `␣There` 0.03, `␣A` 0.03 |
| 20 | …the carpet. The → ? | `␣gardener` | 0.001 | 237 | `␣window` 0.04, `␣man` 0.02, `␣carpet` 0.01, `␣only` 0.01, `␣house` 0.01 |
| 21 | …carpet. The gardener → ? | `␣was` | 0.083 | 2 | `␣had` 0.15, `␣was` 0.08, `,` 0.08, `'s` 0.03, `␣took` 0.01 |
| 22 | …. The gardener was → ? | `␣the` | 0.007 | 21 | `␣not` 0.04, `␣very` 0.02, `␣in` 0.02, `␣able` 0.02, `␣a` 0.02 |
| 23 | …The gardener was the → ? | `␣only` | 0.347 | 1 | `␣only` 0.35, `␣one` 0.16, `␣first` 0.07, `␣last` 0.02, `␣best` 0.02 |
| 24 | …gardener was the only → ? | `␣person` | 0.185 | 2 | `␣one` 0.64, `␣person` 0.19, `␣man` 0.03, `␣thing` 0.01, `␣other` 0.01 |
| 25 | …was the only person → ? | `␣with` | 0.027 | 7 | `␣who` 0.23, `␣in` 0.20, `␣to` 0.09, `␣on` 0.07, `␣present` 0.06 |
| 26 | …the only person with → ? | `␣muddy` | 0.000 | 154 | `␣a` 0.25, `␣the` 0.24, `␣his` 0.05, `␣any` 0.04, `␣time` 0.02 |
| 27 | …only person with muddy → ? | `␣boots` | 0.182 | 3 | `␣hands` 0.23, `␣shoes` 0.21, `␣boots` 0.18, `␣clothes` 0.10, `␣feet` 0.04 |
| 28 | …person with muddy boots → ? | `,` | 0.295 | 1 | `,` 0.29, `.` 0.24, `␣and` 0.16, `␣on` 0.05, `␣to` 0.03 |
| 29 | …with muddy boots, → ? | `␣and` | 0.418 | 1 | `␣and` 0.42, `␣but` 0.15, `␣so` 0.07, `␣a` 0.03, `␣as` 0.02 |
| 30 | …muddy boots, and → ? | `␣he` | 0.198 | 1 | `␣he` 0.20, `␣the` 0.20, `␣she` 0.08, `␣his` 0.06, `␣a` 0.03 |
| 31 | …boots, and he → ? | `␣had` | 0.169 | 2 | `␣was` 0.21, `␣had` 0.17, `␣took` 0.02, `␣could` 0.02, `␣didn` 0.02 |
| 32 | …, and he had → ? | `␣been` | 0.114 | 2 | `␣to` 0.22, `␣been` 0.11, `␣a` 0.06, `␣no` 0.05, `␣never` 0.02 |
| 33 | …and he had been → ? | `␣seen` | 0.002 | 69 | `␣wearing` 0.07, `␣walking` 0.04, `␣working` 0.04, `␣in` 0.02, `␣standing` 0.02 |
| 34 | …he had been seen → ? | `␣near` | 0.002 | 80 | `␣by` 0.09, `␣in` 0.08, `␣walking` 0.07, `␣standing` 0.03, `␣wearing` 0.03 |
| 35 | …had been seen near → ? | `␣the` | 0.708 | 1 | `␣the` 0.71, `␣a` 0.09, `␣his` 0.02, `␣by` 0.01, `␣where` 0.01 |
| 36 | …been seen near the → ? | `␣house` | 0.029 | 6 | `␣window` 0.14, `␣door` 0.07, `␣entrance` 0.04, `␣front` 0.03, `␣garden` 0.03 |
| 37 | …seen near the house → ? | `␣at` | 0.019 | 10 | `.` 0.22, `,` 0.14, `␣by` 0.13, `␣in` 0.04, `␣with` 0.03 |
| 38 | …near the house at → ? | `␣midnight` | 0.001 | 39 | `␣the` 0.28, `␣least` 0.07, `␣a` 0.07, `␣one` 0.07, `␣that` 0.06 |
| 39 | …the house at midnight → ? | `.` | 0.382 | 1 | `.` 0.38, `,` 0.17, `␣by` 0.07, `.\n` 0.05, `␣on` 0.04 |
| 40 | …house at midnight. → ? | `␣The` | 0.209 | 2 | `␣He` 0.24, `␣The` 0.21, `␣His` 0.03, `␣It` 0.03, `␣A` 0.03 |
| 41 | …at midnight. The → ? | `␣detect` | 0.000 | 2961 | `␣gardener` 0.09, `␣house` 0.04, `␣window` 0.04, `␣mud` 0.03, `␣man` 0.03 |
| 42 | …midnight. The detect → ? | `ive` | 0.853 | 1 | `ive` 0.85, `ives` 0.10, `ions` 0.01, `an` 0.00, `␣was` 0.00 |
| 43 | …. The detective → ? | `␣concluded` | 0.000 | 280 | `␣was` 0.15, `␣had` 0.14, `,` 0.08, `'s` 0.04, `␣who` 0.02 |
| 44 | …The detective concluded → ? | `␣that` | 0.756 | 1 | `␣that` 0.76, `␣the` 0.04, `,` 0.04, `:` 0.03, `␣he` 0.03 |
| 45 | …detective concluded that → ? | `␣the` | 0.412 | 1 | `␣the` 0.41, `␣he` 0.16, `␣it` 0.09, `␣there` 0.06, `␣a` 0.04 |
| 46 | …ive concluded that the → ? | `␣gardener` | 0.015 | 9 | `␣mud` 0.07, `␣house` 0.07, `␣window` 0.07, `␣man` 0.03, `␣person` 0.02 |
| 47 | …concluded that the gardener → ? | `␣had` | 0.510 | 1 | `␣had` 0.51, `␣was` 0.29, `'s` 0.05, `,` 0.02, `␣must` 0.02 |
| 48 | …that the gardener had → ? | `␣broken` | 0.004 | 39 | `␣been` 0.30, `␣a` 0.04, `␣just` 0.02, `␣not` 0.02, `␣had` 0.02 |
| 49 | …the gardener had broken → ? | `␣into` | 0.084 | 4 | `␣the` 0.26, `␣a` 0.21, `␣his` 0.11, `␣into` 0.08, `␣up` 0.04 |
| 50 | …gardener had broken into → ? | `␣the` | 0.637 | 1 | `␣the` 0.64, `␣a` 0.16, `␣his` 0.09, `␣one` 0.01, `␣an` 0.01 |
| 51 | …had broken into the → ? | `␣study` | 0.000 | 1090 | `␣house` 0.34, `␣window` 0.07, `␣garden` 0.03, `␣home` 0.03, `␣mud` 0.03 |
| 52 | …broken into the study → ? | `.` | 0.076 | 5 | `,` 0.13, `␣by` 0.09, `␣room` 0.09, `␣and` 0.08, `.` 0.08 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.519 | 1 | `.` 0.52, `!` 0.03, `)` 0.02, `).` 0.01, `?` 0.01 |
| 2 | ? ← . | `␣study` | 0.000 | 385 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣Yes` 0.00, `␣years` 0.00 |
| 3 | ? ← study. | `␣the` | 0.281 | 1 | `␣the` 0.28, `␣this` 0.08, `␣of` 0.07, `␣further` 0.04, `␣to` 0.03 |
| 4 | ? ← the study. | `␣into` | 0.003 | 18 | `␣of` 0.32, `␣in` 0.28, `␣to` 0.11, `␣for` 0.06, `␣on` 0.02 |
| 5 | ? ← into the study. | `␣broken` | 0.000 | 1307 | `␣months` 0.04, `␣years` 0.03, `␣incorporated` 0.03, `␣input` 0.02, `␣going` 0.02 |
| 6 | ? ← broken into the study… | `␣had` | 0.020 | 11 | `␣be` 0.18, `␣were` 0.07, `␣are` 0.07, `␣is` 0.07, `␣was` 0.06 |
| 7 | ? ← had broken into the… | `␣gardener` | 0.000 | 10108 | `␣they` 0.12, `␣that` 0.08, `␣who` 0.04, `␣he` 0.04, `␣it` 0.03 |
| 8 | ? ← gardener had broken into… | `␣the` | 0.325 | 1 | `␣the` 0.32, `␣a` 0.09, `␣The` 0.04, `␣master` 0.04, `␣one` 0.02 |
| 9 | ? ← the gardener had broken… | `␣that` | 0.119 | 2 | `␣if` 0.14, `␣that` 0.12, `␣after` 0.10, `,` 0.06, `␣and` 0.04 |
| 10 | ? ← that the gardener had… | `␣concluded` | 0.001 | 107 | `␣mentioned` 0.03, `␣fact` 0.02, `␣said` 0.02, `␣found` 0.02, `␣and` 0.02 |
| 11 | ? ← concluded that the gardener… | `ive` | 0.000 | 1470 | `␣and` 0.09, `␣They` 0.08, `␣author` 0.06, `␣He` 0.05, `␣they` 0.04 |
| 12 | ? ← ive concluded that the… | `␣detect` | 0.499 | 1 | `␣detect` 0.50, `h` 0.04, `␣mot` 0.04, `␣Collect` 0.04, `␣direct` 0.03 |
| 13 | ? ← detective concluded that… | `␣The` | 0.431 | 1 | `␣The` 0.43, `␣the` 0.37, `The` 0.02, `␣a` 0.02, `␣police` 0.01 |
| 14 | ? ← The detective concluded… | `.` | 0.130 | 2 | `:` 0.85, `.` 0.13, `."` 0.01, `).` 0.00, `)` 0.00 |
| 15 | ? ← . The detective… | `␣midnight` | 0.000 | 6828 | `␣garden` 0.03, `␣plants` 0.01, `␣it` 0.01, `␣gardener` 0.01, `␣not` 0.01 |
| 16 | ? ← midnight. The detect… | `␣at` | 0.306 | 1 | `␣at` 0.31, `␣after` 0.19, `␣before` 0.12, `␣around` 0.08, `␣until` 0.05 |
| 17 | ? ← at midnight. The… | `␣house` | 0.012 | 4 | `␣garden` 0.05, `,` 0.03, `␣bed` 0.01, `␣house` 0.01, `␣was` 0.01 |
| 18 | ? ← house at midnight.… | `␣the` | 0.388 | 1 | `␣the` 0.39, `'s` 0.22, `␣his` 0.09, `␣her` 0.06, `␣their` 0.06 |
| 19 | ? ← the house at midnight… | `␣near` | 0.008 | 18 | `␣in` 0.20, `␣of` 0.14, `␣to` 0.10, `␣into` 0.09, `␣left` 0.05 |
| 20 | ? ← near the house at… | `␣seen` | 0.002 | 71 | `␣was` 0.05, `␣found` 0.03, `␣tree` 0.02, `␣appeared` 0.02, `␣garden` 0.02 |
| 21 | ? ← seen near the house… | `␣been` | 0.052 | 4 | `␣was` 0.50, `␣were` 0.21, `␣be` 0.07, `␣been` 0.05, `␣being` 0.02 |
| 22 | ? ← been seen near the… | `␣had` | 0.850 | 1 | `␣had` 0.85, `␣have` 0.06, `␣having` 0.01, `␣already` 0.01, `␣has` 0.01 |
| 23 | ? ← had been seen near… | `␣he` | 0.013 | 8 | `␣that` 0.04, `␣cat` 0.03, `,` 0.03, `␣they` 0.02, `␣bird` 0.02 |
| 24 | ? ← he had been seen… | `␣and` | 0.068 | 3 | `␣that` 0.46, `␣because` 0.07, `␣and` 0.07, `␣said` 0.06, `␣as` 0.05 |
| 25 | ? ← and he had been… | `,` | 0.483 | 1 | `,` 0.48, `␣night` 0.02, `␣garden` 0.02, `␣day` 0.02, `␣morning` 0.01 |
| 26 | ? ← , and he had… | `␣boots` | 0.000 | 1525 | `␣garden` 0.03, `␣night` 0.03, `␣day` 0.02, `␣house` 0.02, `ive` 0.01 |
| 27 | ? ← boots, and he… | `␣muddy` | 0.005 | 31 | `␣his` 0.36, `␣and` 0.05, `'s` 0.05, `␣the` 0.03, `␣rubber` 0.03 |
| 28 | ? ← muddy boots, and… | `␣with` | 0.088 | 4 | `␣his` 0.33, `␣in` 0.10, `␣and` 0.09, `␣with` 0.09, `␣wearing` 0.06 |
| 29 | ? ← with muddy boots,… | `␣person` | 0.003 | 52 | `␣man` 0.07, `␣garden` 0.05, `,` 0.04, `␣house` 0.03, `␣bed` 0.02 |
| 30 | ? ← person with muddy boots… | `␣only` | 0.006 | 13 | `␣a` 0.63, `␣the` 0.07, `␣another` 0.03, `␣old` 0.02, `␣black` 0.01 |
| 31 | ? ← only person with muddy… | `␣the` | 0.983 | 1 | `␣the` 0.98, `␣and` 0.01, `'s` 0.00, `,` 0.00, `␣The` 0.00 |
| 32 | ? ← the only person with… | `␣was` | 0.524 | 1 | `␣was` 0.52, `␣not` 0.20, `'t` 0.09, `␣been` 0.05, `,` 0.03 |
| 33 | ? ← was the only person… | `␣gardener` | 0.093 | 3 | `␣he` 0.31, `␣He` 0.16, `␣gardener` 0.09, `,` 0.03, `␣man` 0.02 |
| 34 | ? ← gardener was the only… | `␣The` | 0.417 | 2 | `␣the` 0.47, `␣The` 0.42, `The` 0.03, `␣a` 0.01, `'s` 0.00 |
| 35 | ? ← The gardener was the… | `.` | 0.878 | 1 | `.` 0.88, `:` 0.06, `."` 0.02, `).` 0.01, `?` 0.00 |
| 36 | ? ← . The gardener was… | `␣carpet` | 0.000 | 1780 | `␣house` 0.04, `␣boots` 0.02, `␣garden` 0.02, `ive` 0.02, `␣night` 0.01 |
| 37 | ? ← carpet. The gardener… | `␣the` | 0.319 | 1 | `␣the` 0.32, `␣red` 0.18, `␣a` 0.06, `␣his` 0.04, `␣green` 0.03 |
| 38 | ? ← the carpet. The… | `␣on` | 0.407 | 1 | `␣on` 0.41, `␣in` 0.09, `␣under` 0.08, `␣of` 0.07, `␣from` 0.04 |
| 39 | ? ← on the carpet.… | `␣mud` | 0.034 | 2 | `␣blood` 0.05, `␣mud` 0.03, `␣dirt` 0.03, `␣lying` 0.03, `␣walking` 0.03 |
| 40 | ? ← mud on the carpet… | `␣was` | 0.070 | 3 | `␣of` 0.28, `␣the` 0.13, `␣was` 0.07, `␣found` 0.05, `␣some` 0.04 |
| 41 | ? ← was mud on the… | `␣there` | 0.570 | 1 | `␣there` 0.57, `␣There` 0.33, `There` 0.07, `␣it` 0.00, `there` 0.00 |
| 42 | ? ← there was mud on… | `␣and` | 0.408 | 1 | `␣and` 0.41, `␣that` 0.27, `,` 0.09, `␣because` 0.03, `␣but` 0.03 |
| 43 | ? ← and there was mud… | `,` | 0.705 | 1 | `,` 0.70, `␣house` 0.01, `␣muddy` 0.01, `␣boots` 0.01, `;` 0.01 |
| 44 | ? ← , and there was… | `␣outside` | 0.009 | 14 | `␣house` 0.04, `␣muddy` 0.03, `␣boots` 0.03, `␣mud` 0.02, `␣dirty` 0.01 |
| 45 | ? ← outside, and there… | `␣the` | 0.024 | 7 | `␣was` 0.06, `␣from` 0.04, `␣went` 0.04, `␣cold` 0.03, `␣dark` 0.03 |
| 46 | ? ← the outside, and… | `␣from` | 0.201 | 2 | `␣on` 0.47, `␣from` 0.20, `␣to` 0.17, `␣around` 0.02, `␣than` 0.01 |
| 47 | ? ← from the outside,… | `␣open` | 0.002 | 50 | `␣seen` 0.10, `␣house` 0.06, `␣visible` 0.05, `␣coming` 0.03, `␣wet` 0.02 |
| 48 | ? ← open from the outside… | `␣forced` | 0.000 | 166 | `␣was` 0.20, `␣were` 0.12, `␣cracked` 0.05, `␣ripped` 0.04, `␣broken` 0.04 |
| 49 | ? ← forced open from the… | `␣been` | 0.413 | 1 | `␣been` 0.41, `␣was` 0.29, `␣were` 0.15, `␣being` 0.03, `␣had` 0.03 |
| 50 | ? ← been forced open from… | `␣had` | 0.962 | 1 | `␣had` 0.96, `␣just` 0.01, `␣not` 0.01, `␣already` 0.00, `had` 0.00 |
| 51 | ? ← had been forced open… | `␣window` | 0.043 | 5 | `␣door` 0.29, `␣house` 0.07, `␣doors` 0.07, `␣windows` 0.05, `␣window` 0.04 |
| 52 | ? ← window had been forced… | `The` | 0.016 | 5 | `␣The` 0.36, `␣the` 0.19, `␣A` 0.12, `␣a` 0.07, `The` 0.02 |

---

## 11. lost_dog

*Category: narrative*

> **Beginning:** When Max the dog went missing, the whole street joined the search.  
> **Middle:** They checked the park, the woods and the river bank until it grew dark.  
> **Ending:** The next morning, Max was found asleep in the neighbour's garden shed.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | , it was clear to me that something was wrong with him. When I saw him, it was clear to me that something was wrong with him. When I saw him, it was clear to me that something was wrong with him. When I saw him, it was clear to me that something was wrong with him, and it was up to me to see what was wrong with him. I quickly realised what was wrong with him, and decided to put Max back at home. ↵  ↵ | The next morning, Max was found asleep in the neighbour's garden shed. |
| sample | discovered an eight year old dog named Max after his parents died. His mother died at 12 weeks, and his father died at 10 weeks. ↵  ↵ He explained that Max died in March 2013, after being separated from her mother at 14 weeks. He then decided to move the baby away from the baby to share with her mother. ↵  ↵ He also revealed that Max has owned multiple pets in the past four weeks, and had difficulty adapting to living in a neighbour's home. ↵  ↵ | The next morning, Max was found asleep in the neighbour's garden shed. |
| sample | her to me, she was not like a terrier. ↵ Since she was such a large dog, when I presented to her, she was treated just like any other dog. ↵ On further research, I learned that she has a short life span, about 15 years, which is all the better for her. ↵ One day, I heard good news. But the next day, I learned that it happened to a tiny terrier named Max, who was just five years old at the time. ↵ | The next morning, Max was found asleep in the neighbour's garden shed. |
| sample | She had told him to give it to her, and he had told her not to give it to him. He had told her not to give this to the dog, as she knew it had been eaten by the dog. Even though she had told him that it had been eaten by the dog, she had told him to not give it to her, and he had told her not to give it to the dog. She was upset, as she had not thought about him. ↵ | The next morning, Max was found asleep in the neighbour's garden shed. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | When Max the dog went missing, the whole street joined the search. | He was a dog that had been missing for a long time. He was a dog that had been missing for a long time. He was a dog that had been missing for a long time. He was a dog that had been missing for a long time. He was a dog that had been missing for a long time. He was a dog that had been missing for a long time. He was a dog that had been missing for a long time. He was a dog that |
| sample | When Max the dog went missing, the whole street joined the search. | He was just a few meters from the gate, and the police saw him on the sidewalk. "He's a stray dog," Max said. He was an indoor dog, but he needed a lot of space to roam. The two neighbors were worried about him, and Max was only a few centimeters from the gate. He was a rescue dog, but he was never fully adopted. " He's just a few centimeters," the police said. ↵ Max was abandoned when he was less |
| sample | When Max the dog went missing, the whole street joined the search. | The local police were on the scene. They searched to find Max and told everyone they knew they were lost. They didn't find Max. Everyone thought he was lost. Max was rescued by the police. But when Max went missing, police and all other people were on the scene. ↵ "Why did Max go missing?" police said. "It's an old dog, so we can't trust him. He's old, but he was found by the police and is now alive |
| sample | When Max the dog went missing, the whole street joined the search. | The search turned to the north, a place for the dog where his human was not found. The search was not stopped, but the dog was found, a dog that was not afraid of people who were not near him. He ran from the house to the tree where the tree was located, turned around, looked at a strange animal, and looked at the tree again. He was surprised by the animal, as it was a dog that had been waiting for a long time for |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 1.138 | 38% |
| Backward | previous-token (right context) | 1.162 | 29% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `When` | 0.007 | 18 | `The` 0.06, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | When → ? | `␣Max` | 0.000 | 1256 | `␣it` 0.14, `␣you` 0.12, `␣the` 0.08, `␣I` 0.05, `␣a` 0.05 |
| 3 | When Max → ? | `␣the` | 0.005 | 25 | `␣and` 0.08, `im` 0.07, `␣was` 0.05, `ine` 0.05, `␣is` 0.04 |
| 4 | When Max the → ? | `␣dog` | 0.039 | 2 | `␣Dog` 0.05, `␣dog` 0.04, `␣Cat` 0.02, `␣cat` 0.02, `␣Dinosaur` 0.01 |
| 5 | When Max the dog → ? | `␣went` | 0.008 | 16 | `␣was` 0.15, `␣is` 0.11, `'s` 0.03, `␣first` 0.02, `␣started` 0.02 |
| 6 | …Max the dog went → ? | `␣missing` | 0.044 | 6 | `␣to` 0.42, `␣on` 0.07, `␣into` 0.06, `␣for` 0.05, `␣out` 0.05 |
| 7 | …the dog went missing → ? | `,` | 0.386 | 1 | `,` 0.39, `␣in` 0.18, `␣he` 0.05, `␣for` 0.04, `␣on` 0.03 |
| 8 | …dog went missing, → ? | `␣the` | 0.116 | 2 | `␣he` 0.27, `␣his` 0.12, `␣the` 0.12, `␣it` 0.04, `␣I` 0.03 |
| 9 | …went missing, the → ? | `␣whole` | 0.006 | 21 | `␣police` 0.06, `␣owner` 0.05, `␣family` 0.04, `␣team` 0.02, `␣authorities` 0.02 |
| 10 | …missing, the whole → ? | `␣street` | 0.000 | 183 | `␣family` 0.24, `␣world` 0.14, `␣town` 0.06, `␣neighborhood` 0.05, `␣community` 0.04 |
| 11 | …, the whole street → ? | `␣joined` | 0.000 | 355 | `␣was` 0.49, `␣looked` 0.03, `␣turned` 0.03, `␣went` 0.03, `␣became` 0.02 |
| 12 | …the whole street joined → ? | `␣the` | 0.116 | 3 | `␣him` 0.38, `␣in` 0.20, `␣the` 0.12, `␣together` 0.06, `␣his` 0.05 |
| 13 | …whole street joined the → ? | `␣search` | 0.063 | 1 | `␣search` 0.06, `␣scene` 0.04, `␣dog` 0.02, `␣missing` 0.02, `␣police` 0.02 |
| 14 | …street joined the search → ? | `.` | 0.249 | 1 | `.` 0.25, `␣and` 0.13, `␣party` 0.10, `,` 0.10, `␣for` 0.08 |
| 15 | …joined the search. → ? | `␣They` | 0.013 | 14 | `␣He` 0.12, `␣The` 0.11, `␣It` 0.04, `␣In` 0.03, `␣There` 0.03 |
| 16 | …the search. They → ? | `␣checked` | 0.001 | 139 | `␣were` 0.15, `␣had` 0.08, `␣found` 0.06, `␣searched` 0.03, `␣could` 0.03 |
| 17 | …search. They checked → ? | `␣the` | 0.350 | 1 | `␣the` 0.35, `␣every` 0.08, `␣all` 0.07, `␣out` 0.03, `␣in` 0.03 |
| 18 | …. They checked the → ? | `␣park` | 0.001 | 208 | `␣dog` 0.03, `␣street` 0.02, `␣streets` 0.02, `␣house` 0.02, `␣door` 0.02 |
| 19 | …They checked the park → ? | `,` | 0.283 | 1 | `,` 0.28, `␣and` 0.23, `'s` 0.05, `␣for` 0.05, `.` 0.02 |
| 20 | …checked the park, → ? | `␣the` | 0.201 | 1 | `␣the` 0.20, `␣and` 0.08, `␣but` 0.04, `␣saw` 0.03, `␣checked` 0.03 |
| 21 | …the park, the → ? | `␣woods` | 0.015 | 9 | `␣dog` 0.03, `␣park` 0.02, `␣streets` 0.02, `␣road` 0.02, `␣street` 0.02 |
| 22 | …park, the woods → ? | `␣and` | 0.203 | 2 | `,` 0.74, `␣and` 0.20, `␣behind` 0.01, `␣around` 0.01, `␣near` 0.00 |
| 23 | …, the woods and → ? | `␣the` | 0.426 | 1 | `␣the` 0.43, `␣even` 0.08, `␣all` 0.03, `␣fields` 0.01, `,` 0.01 |
| 24 | …the woods and the → ? | `␣river` | 0.035 | 5 | `␣streets` 0.04, `␣fields` 0.04, `␣road` 0.04, `␣roads` 0.04, `␣river` 0.04 |
| 25 | …woods and the river → ? | `␣bank` | 0.028 | 9 | `.` 0.23, `,` 0.16, `bank` 0.08, `banks` 0.06, `␣and` 0.05 |
| 26 | …and the river bank → ? | `␣until` | 0.004 | 15 | `.` 0.40, `,` 0.20, `␣and` 0.08, `␣for` 0.05, `␣to` 0.05 |
| 27 | …the river bank until → ? | `␣it` | 0.027 | 3 | `␣they` 0.60, `␣the` 0.11, `␣it` 0.03, `␣a` 0.03, `␣all` 0.02 |
| 28 | …river bank until it → ? | `␣grew` | 0.000 | 84 | `␣was` 0.67, `␣became` 0.05, `␣came` 0.04, `␣turned` 0.03, `␣got` 0.02 |
| 29 | …bank until it grew → ? | `␣dark` | 0.193 | 1 | `␣dark` 0.19, `␣too` 0.06, `␣to` 0.05, `␣clear` 0.04, `␣up` 0.03 |
| 30 | …until it grew dark → ? | `.` | 0.357 | 1 | `.` 0.36, `␣and` 0.29, `,` 0.11, `.\n` 0.03, `␣again` 0.03 |
| 31 | …it grew dark. → ? | `␣The` | 0.117 | 2 | `␣They` 0.14, `␣The` 0.12, `␣It` 0.06, `␣Then` 0.05, `␣Max` 0.04 |
| 32 | …grew dark. The → ? | `␣next` | 0.008 | 17 | `␣dog` 0.08, `␣dogs` 0.06, `␣search` 0.05, `␣sun` 0.02, `␣night` 0.02 |
| 33 | …dark. The next → ? | `␣morning` | 0.229 | 2 | `␣day` 0.51, `␣morning` 0.23, `␣night` 0.09, `␣thing` 0.06, `␣time` 0.02 |
| 34 | …. The next morning → ? | `,` | 0.472 | 1 | `,` 0.47, `␣they` 0.22, `␣the` 0.10, `␣Max` 0.04, `␣a` 0.02 |
| 35 | …The next morning, → ? | `␣Max` | 0.064 | 3 | `␣they` 0.29, `␣the` 0.19, `␣Max` 0.06, `␣a` 0.05, `␣when` 0.03 |
| 36 | …next morning, Max → ? | `␣was` | 0.218 | 1 | `␣was` 0.22, `␣and` 0.10, `␣went` 0.08, `'s` 0.04, `,` 0.03 |
| 37 | …morning, Max was → ? | `␣found` | 0.080 | 1 | `␣found` 0.08, `␣gone` 0.05, `␣back` 0.03, `␣seen` 0.02, `␣out` 0.02 |
| 38 | …, Max was found → ? | `␣asleep` | 0.001 | 89 | `␣by` 0.12, `␣in` 0.11, `␣dead` 0.09, `.` 0.08, `␣and` 0.04 |
| 39 | …Max was found asleep → ? | `␣in` | 0.206 | 1 | `␣in` 0.21, `.` 0.15, `␣on` 0.13, `,` 0.10, `␣and` 0.08 |
| 40 | …was found asleep in → ? | `␣the` | 0.578 | 1 | `␣the` 0.58, `␣a` 0.23, `␣his` 0.11, `␣one` 0.02, `␣an` 0.01 |
| 41 | …found asleep in the → ? | `␣neighbour` | 0.000 | 1993 | `␣woods` 0.19, `␣river` 0.13, `␣park` 0.04, `␣middle` 0.04, `␣trees` 0.03 |
| 42 | …asleep in the neighbour → ? | `'s` | 0.955 | 1 | `'s` 0.96, `’s` 0.03, `ly` 0.00, `´s` 0.00, `␣tree` 0.00 |
| 43 | …in the neighbour's → ? | `␣garden` | 0.303 | 1 | `␣garden` 0.30, `␣yard` 0.11, `␣backyard` 0.06, `␣car` 0.06, `␣house` 0.05 |
| 44 | …the neighbour's garden → ? | `␣shed` | 0.001 | 39 | `.` 0.43, `,` 0.18, `.\n` 0.08, `␣and` 0.04, `␣in` 0.03 |
| 45 | …neighbour's garden shed → ? | `.` | 0.458 | 1 | `.` 0.46, `,` 0.19, `.\n` 0.08, `␣and` 0.04, `␣in` 0.03 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.519 | 1 | `.` 0.52, `!` 0.03, `)` 0.02, `).` 0.01, `?` 0.01 |
| 2 | ? ← . | `␣shed` | 0.000 | 6099 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣Yes` 0.00, `␣years` 0.00 |
| 3 | ? ← shed. | `␣garden` | 0.050 | 5 | `␣the` 0.20, `␣a` 0.09, `␣or` 0.07, `␣your` 0.06, `␣garden` 0.05 |
| 4 | ? ← garden shed. | `'s` | 0.003 | 20 | `␣a` 0.24, `␣the` 0.21, `␣or` 0.13, `␣your` 0.12, `␣A` 0.02 |
| 5 | ? ← 's garden shed. | `␣neighbour` | 0.012 | 14 | `␣author` 0.06, `␣one` 0.05, `␣neighbor` 0.03, `␣children` 0.03, `␣friend` 0.02 |
| 6 | ? ← neighbour's garden shed… | `␣the` | 0.210 | 3 | `␣a` 0.35, `␣your` 0.26, `␣the` 0.21, `␣their` 0.03, `␣or` 0.02 |
| 7 | ? ← the neighbour's garden… | `␣in` | 0.299 | 1 | `␣in` 0.30, `␣from` 0.13, `␣at` 0.08, `␣to` 0.07, `␣of` 0.06 |
| 8 | ? ← in the neighbour's… | `␣asleep` | 0.000 | 756 | `␣or` 0.04, `␣it` 0.03, `␣found` 0.03, `␣them` 0.02, `␣stored` 0.02 |
| 9 | ? ← asleep in the neighbour… | `␣found` | 0.014 | 12 | `␣fell` 0.17, `␣was` 0.15, `␣fall` 0.10, `␣is` 0.07, `␣falling` 0.05 |
| 10 | ? ← found asleep in the… | `␣was` | 0.612 | 1 | `␣was` 0.61, `␣were` 0.09, `␣is` 0.04, `␣be` 0.03, `␣been` 0.03 |
| 11 | ? ← was found asleep in… | `␣Max` | 0.000 | 433 | `␣It` 0.16, `␣He` 0.10, `␣She` 0.08, `␣it` 0.07, `␣who` 0.05 |
| 12 | ? ← Max was found asleep… | `,` | 0.110 | 3 | `:` 0.51, `␣named` 0.15, `,` 0.11, `␣when` 0.03, `.` 0.02 |
| 13 | ? ← , Max was found… | `␣morning` | 0.014 | 6 | `␣No` 0.20, `␣Yes` 0.11, `␣day` 0.04, `␣later` 0.02, `␣night` 0.01 |
| 14 | ? ← morning, Max was… | `␣next` | 0.234 | 1 | `␣next` 0.23, `␣the` 0.11, `␣following` 0.08, `␣One` 0.07, `␣this` 0.06 |
| 15 | ? ← next morning, Max… | `␣The` | 0.712 | 1 | `␣The` 0.71, `␣the` 0.19, `The` 0.05, `␣very` 0.03, `.The` 0.00 |
| 16 | ? ← The next morning,… | `.` | 0.618 | 1 | `.` 0.62, `:` 0.34, `!` 0.01, `."` 0.01, `).` 0.01 |
| 17 | ? ← . The next morning… | `␣dark` | 0.001 | 126 | `␣night` 0.03, `␣home` 0.02, `␣bed` 0.02, `␣him` 0.02, `␣house` 0.02 |
| 18 | ? ← dark. The next… | `␣grew` | 0.006 | 13 | `␣the` 0.49, `␣after` 0.20, `␣before` 0.05, `␣was` 0.04, `␣got` 0.02 |
| 19 | ? ← grew dark. The… | `␣it` | 0.109 | 2 | `␣sky` 0.13, `␣it` 0.11, `␣suddenly` 0.07, `␣soon` 0.05, `␣quickly` 0.05 |
| 20 | ? ← it grew dark.… | `␣until` | 0.156 | 2 | `␣as` 0.26, `␣until` 0.16, `␣before` 0.12, `,` 0.09, `␣when` 0.09 |
| 21 | ? ← until it grew dark… | `␣bank` | 0.000 | 683 | `,` 0.05, `␣night` 0.04, `␣waited` 0.03, `␣it` 0.02, `␣bed` 0.02 |
| 22 | ? ← bank until it grew… | `␣river` | 0.049 | 3 | `␣the` 0.56, `␣snow` 0.06, `␣river` 0.05, `␣a` 0.05, `gy` 0.03 |
| 23 | ? ← river bank until it… | `␣the` | 0.791 | 1 | `␣the` 0.79, `␣a` 0.11, `␣nearby` 0.01, `␣muddy` 0.01, `␣dry` 0.00 |
| 24 | ? ← the river bank until… | `␣and` | 0.002 | 26 | `␣on` 0.33, `␣along` 0.20, `␣in` 0.07, `␣near` 0.06, `␣of` 0.05 |
| 25 | ? ← and the river bank… | `␣woods` | 0.004 | 40 | `␣house` 0.07, `,` 0.03, `␣garden` 0.03, `␣trees` 0.02, `␣pond` 0.02 |
| 26 | ? ← woods and the river… | `␣the` | 0.870 | 1 | `␣the` 0.87, `␣nearby` 0.03, `,` 0.01, `␣surrounding` 0.01, `␣local` 0.01 |
| 27 | ? ← the woods and the… | `,` | 0.029 | 9 | `␣in` 0.20, `␣through` 0.18, `␣around` 0.08, `␣into` 0.06, `␣over` 0.04 |
| 28 | ? ← , the woods and… | `␣park` | 0.014 | 10 | `␣house` 0.14, `␣garden` 0.08, `␣field` 0.04, `␣fields` 0.04, `␣road` 0.03 |
| 29 | ? ← park, the woods… | `␣the` | 0.760 | 1 | `␣the` 0.76, `␣car` 0.08, `␣a` 0.02, `␣local` 0.02, `␣dog` 0.01 |
| 30 | ? ← the park, the… | `␣checked` | 0.001 | 70 | `␣around` 0.19, `␣in` 0.16, `␣through` 0.11, `␣exploring` 0.06, `,` 0.05 |
| 31 | ? ← checked the park,… | `␣They` | 0.052 | 6 | `␣and` 0.16, `␣Max` 0.13, `␣they` 0.07, `␣he` 0.07, `␣He` 0.06 |
| 32 | ? ← They checked the park… | `.` | 0.958 | 1 | `.` 0.96, `!` 0.01, `."` 0.01, `'.` 0.00, `:` 0.00 |
| 33 | ? ← . They checked the… | `␣search` | 0.000 | 523 | `␣home` 0.02, `␣night` 0.02, `␣house` 0.02, `␣him` 0.02, `␣river` 0.01 |
| 34 | ? ← search. They checked… | `␣the` | 0.187 | 2 | `␣their` 0.37, `␣the` 0.19, `␣to` 0.10, `␣a` 0.07, `␣his` 0.04 |
| 35 | ? ← the search. They… | `␣joined` | 0.032 | 9 | `␣in` 0.09, `␣continue` 0.09, `␣on` 0.09, `␣continued` 0.06, `␣of` 0.06 |
| 36 | ? ← joined the search.… | `␣street` | 0.000 | 635 | `,` 0.08, `␣and` 0.07, `␣Max` 0.05, `␣children` 0.04, `␣had` 0.04 |
| 37 | ? ← street joined the search… | `␣whole` | 0.001 | 44 | `␣the` 0.83, `␣main` 0.01, `␣same` 0.01, `'s` 0.01, `␣nearby` 0.00 |
| 38 | ? ← whole street joined the… | `␣the` | 0.923 | 1 | `␣the` 0.92, `␣The` 0.03, `␣a` 0.02, `The` 0.01, `␣his` 0.00 |
| 39 | ? ← the whole street joined… | `,` | 0.182 | 1 | `,` 0.18, `␣in` 0.10, `␣and` 0.09, `␣across` 0.08, `␣from` 0.05 |
| 40 | ? ← , the whole street… | `␣missing` | 0.000 | 271 | `␣morning` 0.06, `␣day` 0.04, `␣night` 0.04, `␣later` 0.04, `␣evening` 0.02 |
| 41 | ? ← missing, the whole… | `␣went` | 0.245 | 2 | `␣was` 0.30, `␣went` 0.24, `␣were` 0.05, `␣Max` 0.04, `␣still` 0.03 |
| 42 | ? ← went missing, the… | `␣dog` | 0.057 | 3 | `␣Max` 0.53, `␣he` 0.07, `␣dog` 0.06, `,` 0.02, `␣cat` 0.01 |
| 43 | ? ← dog went missing,… | `␣the` | 0.375 | 1 | `␣the` 0.37, `'s` 0.16, `␣their` 0.11, `␣his` 0.10, `␣her` 0.05 |
| 44 | ? ← the dog went missing… | `␣Max` | 0.003 | 23 | `␣When` 0.30, `␣when` 0.19, `When` 0.15, `␣as` 0.07, `␣after` 0.04 |
| 45 | ? ← Max the dog went… | `When` | 0.201 | 3 | `␣when` 0.23, `␣When` 0.23, `When` 0.20, `␣day` 0.03, `␣after` 0.03 |

---

## 12. job_interview

*Category: narrative*

> **Beginning:** Tom spent the whole weekend preparing for his job interview.  
> **Middle:** He researched the company, practised his answers and chose his best suit.  
> **Ending:** On Friday, he received a phone call offering him the position.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | do it, if I want to do it, if I want to do it, if I want to do it, if I want to do it, if I want to do it, if I want to do it, if I want to do it, if I want to do it, if I want to do it, if I want to do it, if I want to do it, if I want to do it, I want to do it," he said. ↵  ↵ | On Friday, he received a phone call offering him the position. |
| sample | and he thinks it has something to do with all of it. ↵  ↵ "It might have to do with all of that, all of this, because you're dealing with the pain, and I tell you when you're dealing with that kind of pain, sure you're comfortable with that, but you don't know how the pain is going to feel, and you just have the feeling of hope that you're going to see it, and the relief that comes from that," he said. ↵  ↵ | On Friday, he received a phone call offering him the position. |
| sample | he said. ↵ And this year, Mike Tyson is their second place winner. This year's third place winner, Mike Tyson, was called out on Monday to talk about the situation. He said he was on the phone, and when asked if they would be interested in opening him up, he said it didn't mean anything to him. ↵ "What I'm saying is if you don't keep talking with you, someone won't believe you," he said on Monday. ↵ | On Friday, he received a phone call offering him the position. |
| sample | to me. ↵ Granted, since he is 21, and he is in high school, this is not a new thing for him. But he has been involved in the community for a long time, and he knows that it has always been that way. “I have probably never heard of it,” he said. “Well, I want to know all about it,” he said. ↵ “Well, that is my job; I'm on my way,” he said. ↵ | On Friday, he received a phone call offering him the position. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | Tom spent the whole weekend preparing for his job interview. | He was a very good cook, but he was also a very good cook. He was a very good cook, but he was also a very good cook. He was a very good cook, but he was also a very good cook. He was a very good cook, but he was also a very good cook. He was a very good cook, but he was also a very good cook. He was a very good cook, but he was also a very good cook. |
| sample | Tom spent the whole weekend preparing for his job interview. | He was able to work the same jobs. At the same time, he didn't feel like spending a lot of time doing the things he wanted to do, and he didn't feel like being lazy. So I asked him, "I'm a computer programmer, why do I have to do something I like?" He said, "I want to do something that computers don't do." And I said, "Why not just do it? I don't want to do that |
| sample | Tom spent the whole weekend preparing for his job interview. | A recent interview with a friend revealed his life's work with the 80s. The interview also demonstrated how he's been a "safe and determined" guy. He said "I take it lightly when I don't have time." His advice? "I don't want to be a failure because I have a passion." ↵ Tom's work history isn't just his work life, but it's also his life. ↵ Tom has a lot of books he's reading, but not |
| sample | Tom spent the whole weekend preparing for his job interview. | The interview asked the question, "Which of the following is your strongest and most important skill?" The answer was, "I'm a musician." He asked it, "Which of these is your passion?" The answer was, "I'm a musician." ↵ And the question, "Which of these is your hobby?" The answer was, "I'm a musician." ↵ You could have a career in the music industry that involves working with musicians and making music. You can do so in |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.994 | 36% |
| Backward | previous-token (right context) | 1.044 | 36% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `Tom` | 0.000 | 540 | `The` 0.06, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | Tom → ? | `␣spent` | 0.000 | 3527 | `ato` 0.23, `atoes` 0.22, `orrow` 0.19, `at` 0.02, `:` 0.02 |
| 3 | Tom spent → ? | `␣the` | 0.132 | 2 | `␣a` 0.16, `␣the` 0.13, `␣his` 0.11, `␣` 0.11, `␣most` 0.05 |
| 4 | Tom spent the → ? | `␣whole` | 0.016 | 15 | `␣last` 0.16, `␣first` 0.13, `␣summer` 0.10, `␣day` 0.09, `␣next` 0.05 |
| 5 | Tom spent the whole → ? | `␣weekend` | 0.081 | 3 | `␣day` 0.18, `␣summer` 0.12, `␣weekend` 0.08, `␣of` 0.06, `␣week` 0.06 |
| 6 | …spent the whole weekend → ? | `␣preparing` | 0.004 | 30 | `␣in` 0.09, `␣at` 0.07, `␣with` 0.04, `␣trying` 0.03, `␣on` 0.03 |
| 7 | …the whole weekend preparing → ? | `␣for` | 0.375 | 1 | `␣for` 0.37, `␣his` 0.11, `␣the` 0.10, `␣a` 0.06, `␣to` 0.06 |
| 8 | …whole weekend preparing for → ? | `␣his` | 0.232 | 2 | `␣the` 0.32, `␣his` 0.23, `␣a` 0.11, `␣this` 0.03, `␣an` 0.02 |
| 9 | …weekend preparing for his → ? | `␣job` | 0.001 | 118 | `␣first` 0.11, `␣` 0.04, `␣final` 0.03, `␣upcoming` 0.03, `␣trip` 0.03 |
| 10 | …preparing for his job → ? | `␣interview` | 0.257 | 1 | `␣interview` 0.26, `␣at` 0.14, `␣as` 0.11, `,` 0.08, `.` 0.08 |
| 11 | …for his job interview → ? | `.` | 0.290 | 1 | `.` 0.29, `,` 0.18, `␣and` 0.10, `␣at` 0.05, `␣in` 0.05 |
| 12 | …his job interview. → ? | `␣He` | 0.344 | 1 | `␣He` 0.34, `␣The` 0.04, `␣His` 0.04, `␣It` 0.03, `␣"` 0.03 |
| 13 | …job interview. He → ? | `␣researched` | 0.001 | 121 | `␣was` 0.11, `␣had` 0.06, `'s` 0.03, `␣is` 0.03, `␣also` 0.02 |
| 14 | …interview. He researched → ? | `␣the` | 0.267 | 1 | `␣the` 0.27, `␣his` 0.08, `␣and` 0.06, `␣a` 0.04, `,` 0.03 |
| 15 | …. He researched the → ? | `␣company` | 0.061 | 2 | `␣job` 0.07, `␣company` 0.06, `␣interview` 0.03, `␣best` 0.03, `␣latest` 0.01 |
| 16 | …He researched the company → ? | `,` | 0.232 | 1 | `,` 0.23, `␣and` 0.20, `'s` 0.18, `␣he` 0.05, `␣for` 0.03 |
| 17 | …researched the company, → ? | `␣pract` | 0.000 | 921 | `␣the` 0.12, `␣its` 0.11, `␣and` 0.04, `␣read` 0.03, `␣interviewed` 0.02 |
| 18 | …the company, pract → ? | `ised` | 0.945 | 1 | `ised` 0.95, `ising` 0.04, `ic` 0.01, `ized` 0.00, `ises` 0.00 |
| 19 | …company, practised → ? | `␣his` | 0.364 | 1 | `␣his` 0.36, `␣for` 0.11, `␣the` 0.07, `␣interview` 0.04, `,` 0.02 |
| 20 | …, practised his → ? | `␣answers` | 0.006 | 23 | `␣interview` 0.12, `␣skills` 0.12, `␣speaking` 0.06, `␣presentation` 0.03, `␣job` 0.02 |
| 21 | …practised his answers → ? | `␣and` | 0.197 | 2 | `,` 0.38, `␣and` 0.20, `␣to` 0.16, `␣in` 0.08, `␣on` 0.07 |
| 22 | …ised his answers and → ? | `␣chose` | 0.002 | 84 | `␣then` 0.08, `␣got` 0.04, `␣even` 0.03, `␣was` 0.03, `␣answered` 0.02 |
| 23 | …his answers and chose → ? | `␣his` | 0.056 | 3 | `␣the` 0.57, `␣a` 0.12, `␣his` 0.06, `␣one` 0.03, `␣an` 0.02 |
| 24 | …answers and chose his → ? | `␣best` | 0.139 | 1 | `␣best` 0.14, `␣favourite` 0.08, `␣answer` 0.08, `␣answers` 0.07, `␣favorite` 0.05 |
| 25 | …and chose his best → ? | `␣suit` | 0.000 | 384 | `␣answer` 0.27, `␣answers` 0.15, `.` 0.06, `␣option` 0.03, `␣work` 0.03 |
| 26 | …chose his best suit → ? | `.` | 0.474 | 1 | `.` 0.47, `␣of` 0.12, `␣for` 0.07, `.\n` 0.05, `,` 0.05 |
| 27 | …his best suit. → ? | `␣On` | 0.006 | 24 | `␣He` 0.27, `␣The` 0.07, `␣Tom` 0.04, `␣But` 0.03, `␣It` 0.03 |
| 28 | …best suit. On → ? | `␣Friday` | 0.040 | 4 | `␣the` 0.49, `␣his` 0.11, `␣Monday` 0.04, `␣Friday` 0.04, `␣Saturday` 0.03 |
| 29 | …suit. On Friday → ? | `,` | 0.423 | 1 | `,` 0.42, `␣he` 0.19, `␣morning` 0.09, `␣the` 0.05, `␣night` 0.05 |
| 30 | …. On Friday, → ? | `␣he` | 0.517 | 1 | `␣he` 0.52, `␣Tom` 0.13, `␣the` 0.09, `␣his` 0.02, `␣when` 0.01 |
| 31 | …On Friday, he → ? | `␣received` | 0.007 | 29 | `␣was` 0.14, `␣went` 0.07, `␣got` 0.05, `␣had` 0.03, `␣took` 0.03 |
| 32 | …Friday, he received → ? | `␣a` | 0.399 | 1 | `␣a` 0.40, `␣his` 0.25, `␣the` 0.13, `␣an` 0.12, `␣` 0.01 |
| 33 | …, he received a → ? | `␣phone` | 0.039 | 4 | `␣call` 0.10, `␣letter` 0.07, `␣job` 0.07, `␣phone` 0.04, `␣promotion` 0.02 |
| 34 | …he received a phone → ? | `␣call` | 0.962 | 1 | `␣call` 0.96, `␣interview` 0.00, `␣text` 0.00, `␣number` 0.00, `␣message` 0.00 |
| 35 | …received a phone call → ? | `␣offering` | 0.001 | 32 | `␣from` 0.69, `␣that` 0.03, `␣asking` 0.02, `.` 0.02, `␣telling` 0.02 |
| 36 | …a phone call offering → ? | `␣him` | 0.036 | 6 | `␣a` 0.26, `␣his` 0.10, `␣to` 0.09, `␣advice` 0.07, `␣an` 0.04 |
| 37 | …phone call offering him → ? | `␣the` | 0.053 | 5 | `␣a` 0.38, `␣$` 0.07, `␣his` 0.07, `␣an` 0.06, `␣the` 0.05 |
| 38 | …call offering him the → ? | `␣position` | 0.023 | 6 | `␣opportunity` 0.26, `␣chance` 0.15, `␣job` 0.10, `␣best` 0.04, `␣perfect` 0.03 |
| 39 | …offering him the position → ? | `.` | 0.212 | 2 | `␣of` 0.37, `.` 0.21, `.\n` 0.08, `␣he` 0.05, `,` 0.03 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.519 | 1 | `.` 0.52, `!` 0.03, `)` 0.02, `).` 0.01, `?` 0.01 |
| 2 | ? ← . | `␣position` | 0.000 | 311 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣Yes` 0.00, `␣years` 0.00 |
| 3 | ? ← position. | `␣the` | 0.031 | 1 | `␣the` 0.03, `'s` 0.03, `␣and` 0.02, `␣their` 0.02, `␣in` 0.02 |
| 4 | ? ← the position. | `␣him` | 0.000 | 631 | `␣of` 0.16, `␣for` 0.11, `␣in` 0.11, `␣to` 0.10, `␣at` 0.03 |
| 5 | ? ← him the position. | `␣offering` | 0.009 | 20 | `␣give` 0.14, `␣cost` 0.12, `␣gave` 0.07, `␣offered` 0.04, `␣offer` 0.04 |
| 6 | ? ← offering him the position… | `␣call` | 0.000 | 357 | `,` 0.09, `␣before` 0.09, `␣and` 0.08, `␣for` 0.08, `␣by` 0.06 |
| 7 | ? ← call offering him the… | `␣phone` | 0.088 | 2 | `␣a` 0.18, `␣phone` 0.09, `␣the` 0.09, `␣to` 0.06, `␣telephone` 0.04 |
| 8 | ? ← phone call offering him… | `␣a` | 0.586 | 1 | `␣a` 0.59, `␣the` 0.07, `␣or` 0.02, `␣A` 0.01, `␣return` 0.01 |
| 9 | ? ← a phone call offering… | `␣received` | 0.130 | 1 | `␣received` 0.13, `␣to` 0.07, `␣got` 0.05, `␣made` 0.05, `␣on` 0.04 |
| 10 | ? ← received a phone call… | `␣he` | 0.180 | 1 | `␣he` 0.18, `␣He` 0.14, `␣and` 0.07, `␣had` 0.03, `␣has` 0.02 |
| 11 | ? ← he received a phone… | `,` | 0.276 | 1 | `,` 0.28, `␣when` 0.19, `␣after` 0.08, `␣that` 0.06, `␣and` 0.05 |
| 12 | ? ← , he received a… | `␣Friday` | 0.001 | 165 | `␣Yes` 0.13, `␣later` 0.06, `␣No` 0.05, `␣day` 0.03, `␣time` 0.01 |
| 13 | ? ← Friday, he received… | `␣On` | 0.340 | 1 | `␣On` 0.34, `␣on` 0.25, `␣Last` 0.07, `␣last` 0.06, `On` 0.03 |
| 14 | ? ← On Friday, he… | `.` | 0.806 | 1 | `.` 0.81, `:` 0.14, `."` 0.02, `).` 0.01, `".` 0.00 |
| 15 | ? ← . On Friday,… | `␣suit` | 0.001 | 224 | `␣said` 0.01, `␣him` 0.01, `␣position` 0.01, `␣week` 0.01, `␣Friday` 0.01 |
| 16 | ? ← suit. On Friday… | `␣best` | 0.001 | 94 | `␣the` 0.22, `␣follow` 0.09, `␣a` 0.07, `␣followed` 0.07, `␣his` 0.05 |
| 17 | ? ← best suit. On… | `␣his` | 0.494 | 1 | `␣his` 0.49, `␣the` 0.25, `'s` 0.06, `␣their` 0.02, `␣to` 0.02 |
| 18 | ? ← his best suit.… | `␣chose` | 0.001 | 74 | `␣be` 0.12, `␣in` 0.11, `␣was` 0.10, `␣is` 0.09, `␣not` 0.09 |
| 19 | ? ← chose his best suit… | `␣and` | 0.224 | 2 | `␣he` 0.25, `␣and` 0.22, `␣He` 0.05, `,` 0.03, `␣then` 0.02 |
| 20 | ? ← and chose his best… | `␣answers` | 0.000 | 283 | `,` 0.15, `␣position` 0.02, `␣options` 0.01, `␣interview` 0.01, `␣suit` 0.01 |
| 21 | ? ← answers and chose his… | `␣his` | 0.080 | 2 | `␣the` 0.33, `␣his` 0.08, `␣for` 0.06, `␣several` 0.05, `␣of` 0.04 |
| 22 | ? ← his answers and chose… | `ised` | 0.001 | 83 | `␣reviewed` 0.15, `␣checked` 0.08, `␣all` 0.06, `␣considered` 0.06, `␣of` 0.05 |
| 23 | ? ← ised his answers and… | `␣pract` | 0.015 | 8 | `in` 0.36, `␣summar` 0.20, `␣final` 0.13, `␣appra` 0.08, `␣memor` 0.05 |
| 24 | ? ← practised his answers… | `,` | 0.111 | 3 | `␣he` 0.27, `␣He` 0.12, `,` 0.11, `␣then` 0.03, `He` 0.02 |
| 25 | ? ← , practised his… | `␣company` | 0.001 | 105 | `␣questions` 0.05, `␣interview` 0.02, `␣week` 0.02, `␣Friday` 0.01, `␣him` 0.01 |
| 26 | ? ← company, practised… | `␣the` | 0.444 | 1 | `␣the` 0.44, `␣his` 0.06, `␣insurance` 0.03, `␣a` 0.03, `'s` 0.01 |
| 27 | ? ← the company, pract… | `␣researched` | 0.014 | 15 | `␣of` 0.14, `␣at` 0.10, `␣in` 0.10, `␣with` 0.10, `␣to` 0.08 |
| 28 | ? ← researched the company,… | `␣He` | 0.162 | 2 | `␣he` 0.18, `␣He` 0.16, `,` 0.08, `␣has` 0.07, `He` 0.05 |
| 29 | ? ← He researched the company… | `.` | 0.936 | 1 | `.` 0.94, `."` 0.01, `:` 0.01, `".` 0.01, `?` 0.01 |
| 30 | ? ← . He researched the… | `␣interview` | 0.012 | 3 | `␣position` 0.02, `␣company` 0.02, `␣interview` 0.01, `␣job` 0.01, `␣suit` 0.01 |
| 31 | ? ← interview. He researched… | `␣job` | 0.128 | 3 | `␣an` 0.30, `␣the` 0.19, `␣job` 0.13, `␣his` 0.04, `␣phone` 0.02 |
| 32 | ? ← job interview. He… | `␣his` | 0.076 | 2 | `␣a` 0.61, `␣his` 0.08, `␣the` 0.05, `␣first` 0.02, `␣mock` 0.02 |
| 33 | ? ← his job interview.… | `␣for` | 0.490 | 1 | `␣for` 0.49, `␣before` 0.10, `␣during` 0.07, `␣in` 0.07, `␣to` 0.06 |
| 34 | ? ← for his job interview… | `␣preparing` | 0.081 | 2 | `␣prepare` 0.09, `␣preparing` 0.08, `␣time` 0.03, `␣ready` 0.03, `␣prepared` 0.03 |
| 35 | ? ← preparing for his job… | `␣weekend` | 0.004 | 27 | `␣was` 0.37, `,` 0.05, `␣while` 0.05, `␣busy` 0.04, `␣is` 0.04 |
| 36 | ? ← weekend preparing for his… | `␣whole` | 0.018 | 7 | `␣the` 0.69, `␣this` 0.06, `␣a` 0.05, `␣his` 0.04, `␣last` 0.03 |
| 37 | ? ← whole weekend preparing for… | `␣the` | 0.825 | 1 | `␣the` 0.82, `␣a` 0.15, `␣his` 0.01, `␣spent` 0.00, `␣this` 0.00 |
| 38 | ? ← the whole weekend preparing… | `␣spent` | 0.895 | 1 | `␣spent` 0.90, `␣spend` 0.03, `␣spending` 0.02, `␣almost` 0.01, `ent` 0.00 |
| 39 | ? ← spent the whole weekend… | `Tom` | 0.000 | 294 | `␣He` 0.09, `,` 0.08, `␣he` 0.07, `␣had` 0.06, `␣and` 0.05 |

---

## 13. photosynthesis

*Category: factual*

> **Beginning:** Plants capture energy from sunlight using a pigment called chlorophyll.  
> **Middle:** In a process called photosynthesis, they use this energy to turn carbon dioxide and water into glucose.  
> **Ending:** Oxygen is released into the air as a by-product of this process.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | water into hydrogen and oxygen. ↵ In this process, solar energy is used to split water into hydrogen and oxygen. ↵ In this process, solar energy is used to split water into hydrogen and oxygen. ↵ This is an example of a chemical reaction. ↵ A chemical reaction is a process that converts one form of energy into another form of energy. ↵ An example of this process is the production of hydrogen and oxygen from water. ↵ In this process, solar energy is used to split water into hydrogen and oxygen. ↵ | Oxygen is released into the air as a by-product of this process. |
| sample | ochemistry and Cell Biology, Harvard Medical School, and her team of researchers are hard at work. Their research is contributing to our understanding of how green plants produce their own food through photosynthesis. This knowledge is vital to our understanding of the processes that shape our planet and are home to virtually all life on Earth. ↵ During photosynthesis, green plants produce their own food, using sunlight, water, carbon dioxide and light energy, through a process called photosynthesis. This converts carbon dioxide into pure oxygen. ↵ | Oxygen is released into the air as a by-product of this process. |
| sample | respiration in a cell is accomplished by passing an electric current through the cell. This causes a chemical reaction within the cell, which then produces electrical energy. ↵  ↵ The two most common gases involved in energy production are oxygen and carbon dioxide. ↵  ↵ Carbon Dioxide ↵  ↵ Carbon dioxide is a compound of carbon, hydrogen, and oxygen. Carbon dioxide is formed when the gas is exposed to oxygen. It reacts with the oxygen and combines with oxygen, forming carbon dioxide, methane, and other organic compounds. ↵  ↵ | Oxygen is released into the air as a by-product of this process. |
| sample | oxygen gas. ↵  ↵ During this process, CO2 is released into the air, which requires a lot of energy. ↵  ↵ Question 5 ↵  ↵ The term 'reduction' refers to the conversion of carbon dioxide and water into oxygen using only oxygen and energy. ↵  ↵ In this process, the source of energy is oxygen, and the waste product is carbon dioxide and water. ↵  ↵ Question 6 ↵  ↵ The function of a reactor in a nuclear power plant is to absorb carbon dioxide and replace with the new oxygen. ↵  ↵ | Oxygen is released into the air as a by-product of this process. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | Plants capture energy from sunlight using a pigment called chlorophyll. | The energy is then used to make food for the plant. The energy is stored in the plant's cells. The energy is then used to make food for the plant. The energy is stored in the plant's cells. The energy is stored in the plant's cells. The energy is stored in the plant's cells. The energy is stored in the plant's cells. The energy is stored in the plant's cells. The energy is stored in the plant's cells. The energy |
| sample | Plants capture energy from sunlight using a pigment called chlorophyll. | The energy absorbed by chlorophyll is transferred to its interior molecules, which contain another substance called carotene. ↵  ↵ Plants take in this energy and convert it into sugars using photosynthesis. When the sugars are available, they grow, providing the plant with sugar to use in the next stage of its life cycle. ↵  ↵ The sugar produced from photosynthesis is then used by the plant to produce starch, which is the main food source for the plant and provides its structural support. ↵  ↵ Carotene as a pigment ↵  ↵ Most |
| sample | Plants capture energy from sunlight using a pigment called chlorophyll. | This photosynthetic process is essential for plants to survive, not only because it allows them to produce food but also because it helps them to grow. Researchers from TU Vienna have now succeeded in creating a fluorescent dye that can be used to monitor chlorophyll. Fluorescent dyes are used in a wide range of applications, from molecular biology to biotechnology. The research was published in the journal eLife. ↵  ↵ The importance of chlorophyll ↵  ↵ Chlorophyll is a green pigment that is present in all plants. |
| sample | Plants capture energy from sunlight using a pigment called chlorophyll. | This pigment is a cofactor in photosynthesis for the plant as it is the raw material for the synthesis of glucose. The energy released by the chlorophyll molecule is used to produce ATP. The process, which is described as "the life of the plant", happens in the leaves. The leaves are connected to the plant stem. The process is repeated as the plant grows, just as the stem is connected to the ground. The chlorophyll molecule is responsible for the process. The chloroplast |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.452 | 61% |
| Backward | previous-token (right context) | 0.453 | 57% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `Plants` | 0.000 | 728 | `The` 0.06, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | Plants → ? | `␣capture` | 0.000 | 165 | `␣are` 0.11, `␣and` 0.07, `␣that` 0.04, `␣for` 0.04, `,` 0.04 |
| 3 | Plants capture → ? | `␣energy` | 0.026 | 6 | `␣carbon` 0.31, `␣CO` 0.14, `␣the` 0.08, `␣and` 0.06, `␣light` 0.03 |
| 4 | Plants capture energy → ? | `␣from` | 0.453 | 1 | `␣from` 0.45, `␣in` 0.11, `␣through` 0.07, `␣and` 0.06, `␣by` 0.04 |
| 5 | Plants capture energy from → ? | `␣sunlight` | 0.153 | 2 | `␣the` 0.72, `␣sunlight` 0.15, `␣light` 0.02, `␣sun` 0.02, `␣their` 0.02 |
| 6 | …capture energy from sunlight → ? | `␣using` | 0.062 | 4 | `␣and` 0.29, `,` 0.17, `␣through` 0.08, `␣using` 0.06, `␣to` 0.06 |
| 7 | …energy from sunlight using → ? | `␣a` | 0.245 | 1 | `␣a` 0.24, `␣photosynthesis` 0.12, `␣chlorophyll` 0.11, `␣the` 0.08, `␣their` 0.08 |
| 8 | …from sunlight using a → ? | `␣pigment` | 0.010 | 13 | `␣process` 0.47, `␣complex` 0.04, `␣chemical` 0.04, `␣variety` 0.03, `␣mechanism` 0.03 |
| 9 | …sunlight using a pigment → ? | `␣called` | 0.622 | 1 | `␣called` 0.62, `␣known` 0.10, `,` 0.04, `␣in` 0.04, `␣that` 0.04 |
| 10 | …using a pigment called → ? | `␣chlorophyll` | 0.644 | 1 | `␣chlorophyll` 0.64, `␣phy` 0.14, `␣anth` 0.04, `␣x` 0.02, `␣phot` 0.02 |
| 11 | …a pigment called chlorophyll → ? | `.` | 0.547 | 1 | `.` 0.55, `,` 0.18, `␣and` 0.04, `␣to` 0.04, `␣that` 0.03 |
| 12 | …pigment called chlorophyll. → ? | `␣In` | 0.035 | 5 | `␣The` 0.14, `␣This` 0.10, `␣Chlor` 0.08, `␣Plants` 0.05, `␣In` 0.04 |
| 13 | …called chlorophyll. In → ? | `␣a` | 0.076 | 4 | `␣the` 0.19, `␣this` 0.09, `␣photosynthesis` 0.08, `␣a` 0.08, `␣plants` 0.06 |
| 14 | …chlorophyll. In a → ? | `␣process` | 0.233 | 1 | `␣process` 0.23, `␣plant` 0.07, `␣typical` 0.04, `␣new` 0.04, `␣photosynthetic` 0.02 |
| 15 | …. In a process → ? | `␣called` | 0.659 | 1 | `␣called` 0.66, `␣known` 0.23, `␣that` 0.04, `␣similar` 0.02, `␣termed` 0.01 |
| 16 | …In a process called → ? | `␣photosynthesis` | 0.781 | 1 | `␣photosynthesis` 0.78, `␣phot` 0.08, `␣Photos` 0.05, `␣photos` 0.03, `␣"` 0.01 |
| 17 | …a process called photosynthesis → ? | `,` | 0.950 | 1 | `,` 0.95, `␣plants` 0.01, `␣the` 0.01, `␣that` 0.00, `␣(` 0.00 |
| 18 | …process called photosynthesis, → ? | `␣they` | 0.025 | 5 | `␣plants` 0.52, `␣the` 0.13, `␣a` 0.04, `␣green` 0.03, `␣they` 0.02 |
| 19 | …called photosynthesis, they → ? | `␣use` | 0.162 | 1 | `␣use` 0.16, `␣convert` 0.15, `␣absorb` 0.11, `␣take` 0.09, `␣capture` 0.06 |
| 20 | …photosynthesis, they use → ? | `␣this` | 0.051 | 6 | `␣the` 0.27, `␣sunlight` 0.16, `␣light` 0.12, `␣carbon` 0.09, `␣water` 0.06 |
| 21 | …, they use this → ? | `␣energy` | 0.718 | 1 | `␣energy` 0.72, `␣pigment` 0.09, `␣stored` 0.04, `␣chemical` 0.02, `␣to` 0.02 |
| 22 | …they use this energy → ? | `␣to` | 0.893 | 1 | `␣to` 0.89, `␣and` 0.03, `␣in` 0.02, `,` 0.01, `␣as` 0.01 |
| 23 | …use this energy to → ? | `␣turn` | 0.045 | 6 | `␣make` 0.23, `␣produce` 0.17, `␣convert` 0.12, `␣create` 0.08, `␣grow` 0.06 |
| 24 | …this energy to turn → ? | `␣carbon` | 0.335 | 1 | `␣carbon` 0.34, `␣sunlight` 0.23, `␣water` 0.12, `␣the` 0.10, `␣light` 0.09 |
| 25 | …energy to turn carbon → ? | `␣dioxide` | 0.984 | 1 | `␣dioxide` 0.98, `␣and` 0.00, `␣into` 0.00, `,` 0.00, `␣(` 0.00 |
| 26 | …to turn carbon dioxide → ? | `␣and` | 0.599 | 1 | `␣and` 0.60, `␣into` 0.20, `,` 0.09, `␣(` 0.08, `␣from` 0.01 |
| 27 | …turn carbon dioxide and → ? | `␣water` | 0.980 | 1 | `␣water` 0.98, `␣other` 0.00, `␣hydrogen` 0.00, `␣sunlight` 0.00, `␣oxygen` 0.00 |
| 28 | …carbon dioxide and water → ? | `␣into` | 0.910 | 1 | `␣into` 0.91, `␣and` 0.02, `,` 0.02, `␣(` 0.01, `␣from` 0.01 |
| 29 | …dioxide and water into → ? | `␣glucose` | 0.165 | 3 | `␣sugars` 0.20, `␣oxygen` 0.18, `␣glucose` 0.16, `␣carbohydrates` 0.14, `␣sugar` 0.12 |
| 30 | …and water into glucose → ? | `.` | 0.165 | 3 | `␣and` 0.46, `,` 0.18, `.` 0.17, `␣(` 0.06, `␣for` 0.02 |
| 31 | …water into glucose. → ? | `␣Oxygen` | 0.004 | 37 | `␣The` 0.14, `␣This` 0.13, `␣Plants` 0.06, `␣Photos` 0.05, `␣In` 0.05 |
| 32 | …into glucose. Oxygen → ? | `␣is` | 0.560 | 1 | `␣is` 0.56, `,` 0.07, `␣and` 0.05, `␣from` 0.04, `␣then` 0.03 |
| 33 | …glucose. Oxygen is → ? | `␣released` | 0.125 | 2 | `␣also` 0.15, `␣released` 0.13, `␣produced` 0.12, `␣then` 0.09, `␣the` 0.06 |
| 34 | …. Oxygen is released → ? | `␣into` | 0.077 | 5 | `␣as` 0.25, `␣from` 0.15, `␣during` 0.14, `␣when` 0.14, `␣into` 0.08 |
| 35 | …Oxygen is released into → ? | `␣the` | 0.983 | 1 | `␣the` 0.98, `␣our` 0.00, `␣air` 0.00, `␣a` 0.00, `␣this` 0.00 |
| 36 | …is released into the → ? | `␣air` | 0.438 | 2 | `␣atmosphere` 0.48, `␣air` 0.44, `␣environment` 0.04, `␣surrounding` 0.01, `␣water` 0.00 |
| 37 | …released into the air → ? | `␣as` | 0.253 | 1 | `␣as` 0.25, `␣when` 0.16, `,` 0.14, `␣during` 0.10, `␣and` 0.07 |
| 38 | …into the air as → ? | `␣a` | 0.732 | 1 | `␣a` 0.73, `␣the` 0.10, `␣water` 0.03, `␣carbon` 0.02, `␣by` 0.01 |
| 39 | …the air as a → ? | `␣by` | 0.450 | 1 | `␣by` 0.45, `␣byproduct` 0.37, `␣result` 0.09, `␣waste` 0.07, `␣product` 0.01 |
| 40 | …air as a by → ? | `-product` | 0.917 | 1 | `-product` 0.92, `␣product` 0.08, `product` 0.00, `-` 0.00, `-c` 0.00 |
| 41 | …as a by-product → ? | `␣of` | 0.450 | 1 | `␣of` 0.45, `.` 0.19, `,` 0.12, `.\n` 0.08, `.\n\n` 0.03 |
| 42 | …a by-product of → ? | `␣this` | 0.518 | 1 | `␣this` 0.52, `␣photosynthesis` 0.24, `␣the` 0.16, `␣glucose` 0.02, `␣cellular` 0.01 |
| 43 | …by-product of this → ? | `␣process` | 0.572 | 1 | `␣process` 0.57, `␣reaction` 0.16, `␣glucose` 0.07, `␣chemical` 0.03, `␣photosynthesis` 0.02 |
| 44 | …-product of this process → ? | `.` | 0.443 | 1 | `.` 0.44, `,` 0.21, `.\n` 0.19, `.\n\n` 0.07, `␣and` 0.03 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.519 | 1 | `.` 0.52, `!` 0.03, `)` 0.02, `).` 0.01, `?` 0.01 |
| 2 | ? ← . | `␣process` | 0.002 | 20 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣Yes` 0.00, `␣years` 0.00 |
| 3 | ? ← process. | `␣this` | 0.035 | 2 | `␣the` 0.19, `␣this` 0.04, `␣manufacturing` 0.02, `␣learning` 0.02, `␣production` 0.02 |
| 4 | ? ← this process. | `␣of` | 0.129 | 2 | `␣in` 0.27, `␣of` 0.13, `␣during` 0.10, `␣for` 0.05, `␣through` 0.05 |
| 5 | ? ← of this process. | `-product` | 0.003 | 47 | `␣part` 0.22, `␣result` 0.04, `␣understanding` 0.03, `␣step` 0.02, `␣end` 0.02 |
| 6 | ? ← -product of this process… | `␣by` | 0.884 | 1 | `␣by` 0.88, `␣end` 0.06, `␣bi` 0.02, `␣co` 0.01, `␣side` 0.01 |
| 7 | ? ← by-product of this… | `␣a` | 0.747 | 1 | `␣a` 0.75, `␣the` 0.06, `␣natural` 0.02, `␣important` 0.01, `␣valuable` 0.01 |
| 8 | ? ← a by-product of… | `␣as` | 0.284 | 2 | `␣is` 0.46, `␣as` 0.28, `␣are` 0.09, `␣be` 0.03, `␣also` 0.01 |
| 9 | ? ← as a by-product… | `␣air` | 0.004 | 31 | `␣produced` 0.10, `␣created` 0.07, `␣formed` 0.05, `␣released` 0.04, `␣generated` 0.02 |
| 10 | ? ← air as a by… | `␣the` | 0.601 | 1 | `␣the` 0.60, `␣of` 0.04, `␣and` 0.02, `␣fresh` 0.02, `␣ambient` 0.02 |
| 11 | ? ← the air as a… | `␣into` | 0.533 | 1 | `␣into` 0.53, `␣in` 0.17, `␣from` 0.15, `␣to` 0.07, `␣of` 0.02 |
| 12 | ? ← into the air as… | `␣released` | 0.470 | 1 | `␣released` 0.47, `␣emitted` 0.05, `␣back` 0.04, `␣dioxide` 0.03, `2` 0.02 |
| 13 | ? ← released into the air… | `␣is` | 0.419 | 1 | `␣is` 0.42, `␣are` 0.27, `␣be` 0.11, `␣being` 0.04, `␣also` 0.03 |
| 14 | ? ← is released into the… | `␣Oxygen` | 0.016 | 13 | `␣dioxide` 0.25, `2` 0.12, `␣gas` 0.04, `␣monoxide` 0.04, `␣that` 0.04 |
| 15 | ? ← Oxygen is released into… | `.` | 0.761 | 1 | `.` 0.76, `:` 0.18, `).` 0.02, `)` 0.01, `-` 0.00 |
| 16 | ? ← . Oxygen is released… | `␣glucose` | 0.006 | 26 | `␣oxygen` 0.05, `␣water` 0.04, `␣photosynthesis` 0.03, `␣dioxide` 0.03, `␣energy` 0.02 |
| 17 | ? ← glucose. Oxygen is… | `␣into` | 0.319 | 1 | `␣into` 0.32, `␣and` 0.12, `␣of` 0.11, `␣from` 0.08, `␣to` 0.05 |
| 18 | ? ← into glucose. Oxygen… | `␣water` | 0.052 | 5 | `␣down` 0.18, `␣dioxide` 0.13, `␣carbohydrates` 0.07, `␣converted` 0.06, `␣water` 0.05 |
| 19 | ? ← water into glucose.… | `␣and` | 0.899 | 1 | `␣and` 0.90, `␣split` 0.02, `␣of` 0.01, `␣the` 0.01, `␣convert` 0.01 |
| 20 | ? ← and water into glucose… | `␣dioxide` | 0.861 | 1 | `␣dioxide` 0.86, `,` 0.08, `2` 0.01, `)` 0.01, `␣starch` 0.00 |
| 21 | ? ← dioxide and water into… | `␣carbon` | 0.998 | 1 | `␣carbon` 1.00, `␣Carbon` 0.00, `carbon` 0.00, `␣sulfur` 0.00, `-carbon` 0.00 |
| 22 | ? ← carbon dioxide and water… | `␣turn` | 0.046 | 5 | `␣convert` 0.40, `␣converts` 0.14, `␣converting` 0.11, `,` 0.09, `␣turn` 0.05 |
| 23 | ? ← turn carbon dioxide and… | `␣to` | 0.888 | 1 | `␣to` 0.89, `␣and` 0.02, `␣plants` 0.01, `␣they` 0.01, `␣that` 0.01 |
| 24 | ? ← to turn carbon dioxide… | `␣energy` | 0.130 | 2 | `␣sunlight` 0.35, `␣energy` 0.13, `␣oxygen` 0.08, `␣sun` 0.06, `␣used` 0.05 |
| 25 | ? ← energy to turn carbon… | `␣this` | 0.019 | 9 | `␣light` 0.30, `␣solar` 0.17, `␣chemical` 0.15, `'s` 0.09, `␣sunlight` 0.06 |
| 26 | ? ← this energy to turn… | `␣use` | 0.657 | 1 | `␣use` 0.66, `␣uses` 0.21, `␣using` 0.05, `␣of` 0.04, `␣harness` 0.00 |
| 27 | ? ← use this energy to… | `␣they` | 0.023 | 11 | `␣then` 0.15, `␣plants` 0.14, `␣and` 0.12, `␣cells` 0.10, `␣bacteria` 0.09 |
| 28 | ? ← they use this energy… | `,` | 0.357 | 2 | `␣and` 0.42, `,` 0.36, `␣where` 0.03, `;` 0.03, `␣Then` 0.03 |
| 29 | ? ← , they use this… | `␣photosynthesis` | 0.184 | 1 | `␣photosynthesis` 0.18, `␣sunlight` 0.13, `␣Then` 0.06, `␣oxygen` 0.05, `␣respiration` 0.04 |
| 30 | ? ← photosynthesis, they use… | `␣called` | 0.037 | 8 | `␣During` 0.31, `␣of` 0.17, `␣during` 0.09, `␣perform` 0.08, `␣Through` 0.04 |
| 31 | ? ← called photosynthesis, they… | `␣process` | 0.960 | 1 | `␣process` 0.96, `␣reaction` 0.01, `␣reactions` 0.01, `,` 0.00, `␣is` 0.00 |
| 32 | ? ← process called photosynthesis,… | `␣a` | 0.945 | 1 | `␣a` 0.94, `␣the` 0.03, `␣metabolic` 0.01, `␣chemical` 0.00, `␣another` 0.00 |
| 33 | ? ← a process called photosynthesis… | `␣In` | 0.381 | 1 | `␣In` 0.38, `␣Through` 0.29, `␣in` 0.13, `␣During` 0.09, `␣through` 0.05 |
| 34 | ? ← In a process called… | `.` | 0.966 | 1 | `.` 0.97, `).` 0.02, `:` 0.00, `!` 0.00, `␣.` 0.00 |
| 35 | ? ← . In a process… | `␣chlorophyll` | 0.014 | 8 | `␣sunlight` 0.25, `␣energy` 0.21, `␣sun` 0.15, `␣light` 0.09, `␣photosynthesis` 0.05 |
| 36 | ? ← chlorophyll. In a… | `␣called` | 0.470 | 1 | `␣called` 0.47, `␣pigment` 0.23, `␣contain` 0.04, `␣by` 0.03, `␣using` 0.03 |
| 37 | ? ← called chlorophyll. In… | `␣pigment` | 0.765 | 1 | `␣pigment` 0.77, `␣pigments` 0.07, `␣substance` 0.03, `,` 0.02, `␣cells` 0.01 |
| 38 | ? ← pigment called chlorophyll.… | `␣a` | 0.257 | 2 | `␣green` 0.67, `␣a` 0.26, `␣plant` 0.01, `␣special` 0.01, `␣photosynthetic` 0.01 |
| 39 | ? ← a pigment called chlorophyll… | `␣using` | 0.353 | 1 | `␣using` 0.35, `␣by` 0.16, `␣contain` 0.14, `␣of` 0.08, `␣with` 0.04 |
| 40 | ? ← using a pigment called… | `␣sunlight` | 0.178 | 3 | `␣energy` 0.30, `,` 0.19, `␣sunlight` 0.18, `␣light` 0.13, `␣food` 0.04 |
| 41 | ? ← sunlight using a pigment… | `␣from` | 0.458 | 1 | `␣from` 0.46, `␣absorb` 0.12, `␣of` 0.10, `␣the` 0.10, `␣in` 0.08 |
| 42 | ? ← from sunlight using a… | `␣energy` | 0.967 | 1 | `␣energy` 0.97, `␣food` 0.01, `)` 0.00, `␣light` 0.00, `␣directly` 0.00 |
| 43 | ? ← energy from sunlight using… | `␣capture` | 0.341 | 1 | `␣capture` 0.34, `␣absorb` 0.16, `␣harness` 0.09, `␣the` 0.07, `␣harvest` 0.04 |
| 44 | ? ← capture energy from sunlight… | `Plants` | 0.184 | 2 | `␣plants` 0.39, `Plants` 0.18, `␣Plants` 0.14, `asts` 0.04, `␣leaves` 0.03 |

---

## 14. python_function

*Category: factual*

> **Beginning:** In Python, a function is defined using the def keyword followed by its name.  
> **Middle:** The parameters are listed in parentheses, and the body of the function is indented below the definition.  
> **Ending:** The function sends a value back to the caller using the return statement.

### Generations

**Backward model: given the ending, generate what came before**

| Run | Generated (preceding text) | Given ending |
|---|---|---|
| greedy | The function returns the value that is passed to the function. ↵  ↵ The function returns the value that is passed to the function. ↵  ↵ The function returns the value that is passed to the function. ↵  ↵ The function returns the value that is passed to the function. ↵  ↵ The function returns the value that is passed to the function. ↵  ↵ The function returns the value that is passed to the function. ↵  ↵ The function returns the value that is passed to the function. ↵  ↵ The function returns the value that is passed to the function. ↵  ↵ | The function sends a value back to the caller using the return statement. |
| sample | . ↵  ↵ Explanation ↵  ↵ Here is an example of how to write a function that returns a return back to the caller: ↵  ↵ The return statement is used to return the value of the result of a call to the function. ↵  ↵ The return statement is used to return the value of the result of a call to the function. ↵  ↵ The return statement is used to return the value of the result of the call. ↵  ↵ The return statement is used to return the value of the result of a call to the function. ↵  ↵ | The function sends a value back to the caller using the return statement. |
| sample | = 8 ↵  ↵ If the function returns a value to the caller, then ↵  ↵ System.out.println(); value = 1 ↵  ↵ Else ↵  ↵ System.out.println(); value = 9 ↵  ↵ If the function returns the value to the caller, then ↵  ↵ System.out.println(".", ".", "!") ↵  ↵ Else ↵  ↵ System.out.println(); value = 1 ↵  ↵ End ↵  ↵ | The function sends a value back to the caller using the return statement. |
| sample | function. It is initialized to a string. ↵  ↵ () function parameters ↵  ↵ The function parameters are the set of actions that a function can take during the execution of a function call. These parameters can be used for function calls. ↵  ↵ () return string type ↵  ↵ This is the type of string that will be used during the call. ↵  ↵ () return address ↵  ↵ The second argument is the return address of the value to be returned. It can also be used as a reference for future calls. ↵  ↵ () return ↵  ↵ | The function sends a value back to the caller using the return statement. |

**Forward model: given the beginning, generate what comes after**

| Run | Given beginning | Generated (continuation) |
|---|---|---|
| greedy | In Python, a function is defined using the def keyword followed by its name. | The def keyword is used to define a function. The def keyword is used to define a function. The def keyword is used to define a function. The def keyword is used to define a function. The def keyword is used to define a function. The def keyword is used to define a function. The def keyword is used to define a function. The def keyword is used to define a function. The def keyword is used to define a function. The def keyword is used to |
| sample | In Python, a function is defined using the def keyword followed by its name. | The def keyword is a type for a function called def.def. The Def keyword is used to create a function object with a def name, and return its def value. The def keyword is a common type for a function called def and is used to create a function object with a def name in Python. The def keyword is used to create a function object with a def name in Python. ↵  ↵ In the def keyword, we create a function object with a defined def name. The |
| sample | In Python, a function is defined using the def keyword followed by its name. | For example, the def function in the Python library 'scikit-learn' returns the value of a variable. The def function returns a list of integers from 0 to 9. The def function is a powerful tool in Python's standard library, allowing you to perform various operations on a list of numbers. To define a def function, you can use the def keyword, which provides a list of numbers that the function returns. ↵ Python Syntax for def Function ↵ Definition |
| sample | In Python, a function is defined using the def keyword followed by its name. | For example, if you want to return the product of two vectors (x1 and x2), you can define the function as follows: ↵ def product(x1, x2): ↵ def product(x1, x2): ↵ def sum(count(x1, x2): ↵ def product(x1, x2): ↵ #define f ↵ #define f ↵ #define sum((x1, x2)) ↵ #define sum((x1, x2 |

### Token predictions on the true passage

| Model | Direction | bpb | Top-1 accuracy |
|---|---|---:|---:|
| Forward | next-token (left context) | 0.692 | 54% |
| Backward | previous-token (right context) | 0.782 | 48% |

**Next-token predictions (forward model, read left to right)**

| Step | Left context → ? | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | [start of text] → ? | `In` | 0.021 | 4 | `The` 0.06, `How` 0.03, `What` 0.03, `In` 0.02, `A` 0.02 |
| 2 | In → ? | `␣Python` | 0.000 | 553 | `␣the` 0.22, `␣this` 0.09, `␣` 0.06, `␣a` 0.06, `␣addition` 0.04 |
| 3 | In Python → ? | `,` | 0.672 | 1 | `,` 0.67, `␣` 0.08, `␣we` 0.02, `'s` 0.02, `␣and` 0.01 |
| 4 | In Python, → ? | `␣a` | 0.086 | 3 | `␣the` 0.20, `␣we` 0.12, `␣a` 0.09, `␣you` 0.07, `␣if` 0.02 |
| 5 | In Python, a → ? | `␣function` | 0.059 | 1 | `␣function` 0.06, `␣Python` 0.04, `␣variable` 0.04, `␣list` 0.03, `␣class` 0.03 |
| 6 | …Python, a function → ? | `␣is` | 0.427 | 1 | `␣is` 0.43, `␣can` 0.08, `␣that` 0.04, `'s` 0.02, `␣f` 0.02 |
| 7 | …, a function is → ? | `␣defined` | 0.140 | 2 | `␣a` 0.48, `␣defined` 0.14, `␣an` 0.07, `␣called` 0.04, `␣declared` 0.02 |
| 8 | …a function is defined → ? | `␣using` | 0.039 | 3 | `␣as` 0.59, `␣by` 0.17, `␣using` 0.04, `␣to` 0.03, `␣in` 0.03 |
| 9 | …function is defined using → ? | `␣the` | 0.355 | 1 | `␣the` 0.35, `␣a` 0.33, `␣an` 0.04, `␣its` 0.03, `␣two` 0.02 |
| 10 | …is defined using the → ? | `␣def` | 0.001 | 116 | `␣keyword` 0.06, `␣following` 0.05, `␣function` 0.05, `␣name` 0.04, `␣syntax` 0.02 |
| 11 | …defined using the def → ? | `␣keyword` | 0.438 | 1 | `␣keyword` 0.44, `␣operator` 0.19, `()` 0.04, `␣def` 0.03, `int` 0.03 |
| 12 | …using the def keyword → ? | `␣followed` | 0.023 | 6 | `.` 0.46, `,` 0.17, `␣and` 0.04, `␣as` 0.04, `␣to` 0.02 |
| 13 | …the def keyword followed → ? | `␣by` | 0.992 | 1 | `␣by` 0.99, `␣with` 0.00, `\n` 0.00, `␣in` 0.00, `,` 0.00 |
| 14 | …def keyword followed by → ? | `␣its` | 0.063 | 4 | `␣a` 0.40, `␣the` 0.33, `␣an` 0.08, `␣its` 0.06, `␣two` 0.02 |
| 15 | …keyword followed by its → ? | `␣name` | 0.145 | 2 | `␣arguments` 0.32, `␣name` 0.14, `␣argument` 0.14, `␣parameters` 0.11, `␣return` 0.05 |
| 16 | …followed by its name → ? | `.` | 0.491 | 1 | `.` 0.49, `␣and` 0.15, `,` 0.15, `␣(` 0.03, `.\n` 0.03 |
| 17 | …by its name. → ? | `␣The` | 0.238 | 1 | `␣The` 0.24, `␣For` 0.10, `␣In` 0.07, `␣This` 0.05, `␣A` 0.05 |
| 18 | …its name. The → ? | `␣parameters` | 0.006 | 20 | `␣def` 0.20, `␣function` 0.15, `␣name` 0.14, `␣keyword` 0.03, `␣definition` 0.03 |
| 19 | …name. The parameters → ? | `␣are` | 0.126 | 2 | `␣of` 0.45, `␣are` 0.13, `␣in` 0.06, `␣for` 0.03, `␣to` 0.03 |
| 20 | …. The parameters are → ? | `␣listed` | 0.003 | 45 | `␣passed` 0.12, `␣defined` 0.09, `␣the` 0.08, `␣then` 0.04, `␣given` 0.03 |
| 21 | …The parameters are listed → ? | `␣in` | 0.359 | 1 | `␣in` 0.36, `␣as` 0.21, `␣below` 0.14, `␣under` 0.03, `␣with` 0.03 |
| 22 | …parameters are listed in → ? | `␣parent` | 0.011 | 5 | `␣the` 0.71, `␣a` 0.08, `␣Python` 0.02, `␣an` 0.01, `␣parent` 0.01 |
| 23 | …are listed in parent → ? | `heses` | 0.817 | 1 | `heses` 0.82, `hesis` 0.18, `hes` 0.00, `hetical` 0.00, `hetically` 0.00 |
| 24 | …listed in parentheses → ? | `,` | 0.125 | 2 | `.` 0.29, `,` 0.13, `␣after` 0.12, `.\n` 0.05, `␣and` 0.04 |
| 25 | …in parentheses, → ? | `␣and` | 0.293 | 1 | `␣and` 0.29, `␣followed` 0.07, `␣which` 0.07, `␣with` 0.06, `␣where` 0.05 |
| 26 | …parentheses, and → ? | `␣the` | 0.633 | 1 | `␣the` 0.63, `␣a` 0.04, `␣their` 0.03, `␣you` 0.03, `␣they` 0.02 |
| 27 | …heses, and the → ? | `␣body` | 0.007 | 21 | `␣function` 0.21, `␣arguments` 0.08, `␣return` 0.08, `␣result` 0.05, `␣parameters` 0.03 |
| 28 | …, and the body → ? | `␣of` | 0.725 | 1 | `␣of` 0.72, `␣is` 0.13, `␣contains` 0.02, `␣part` 0.02, `␣(` 0.01 |
| 29 | …and the body of → ? | `␣the` | 0.909 | 1 | `␣the` 0.91, `␣a` 0.04, `␣each` 0.01, `␣that` 0.01, `␣this` 0.01 |
| 30 | …the body of the → ? | `␣function` | 0.913 | 1 | `␣function` 0.91, `␣Python` 0.01, `␣definition` 0.01, `␣parameter` 0.00, `␣def` 0.00 |
| 31 | …body of the function → ? | `␣is` | 0.626 | 1 | `␣is` 0.63, `␣contains` 0.05, `␣defines` 0.02, `␣has` 0.02, `.` 0.02 |
| 32 | …of the function is → ? | `␣ind` | 0.001 | 77 | `␣a` 0.18, `␣the` 0.14, `␣defined` 0.07, `␣enclosed` 0.04, `␣followed` 0.04 |
| 33 | …the function is ind → ? | `ented` | 0.945 | 1 | `ented` 0.95, `ent` 0.03, `entation` 0.01, `eterm` 0.00, `ep` 0.00 |
| 34 | …function is indented → ? | `␣below` | 0.006 | 16 | `␣with` 0.34, `.` 0.25, `␣to` 0.06, `.\n` 0.05, `␣by` 0.05 |
| 35 | …is indented below → ? | `␣the` | 0.594 | 1 | `␣the` 0.59, `.` 0.15, `␣it` 0.04, `␣its` 0.04, `.\n` 0.04 |
| 36 | …indented below the → ? | `␣definition` | 0.033 | 6 | `␣function` 0.21, `␣name` 0.14, `␣parameters` 0.11, `␣parameter` 0.07, `␣parent` 0.07 |
| 37 | …ented below the definition → ? | `.` | 0.528 | 1 | `.` 0.53, `.\n` 0.17, `␣of` 0.08, `.\n\n` 0.03, `,` 0.02 |
| 38 | …below the definition. → ? | `␣The` | 0.264 | 1 | `␣The` 0.26, `␣For` 0.08, `␣In` 0.07, `␣A` 0.04, `␣This` 0.03 |
| 39 | …the definition. The → ? | `␣function` | 0.141 | 1 | `␣function` 0.14, `␣def` 0.08, `␣body` 0.06, `␣parameters` 0.05, `␣name` 0.04 |
| 40 | …definition. The function → ? | `␣sends` | 0.000 | 855 | `␣is` 0.14, `␣name` 0.12, `␣definition` 0.11, `'s` 0.04, `␣body` 0.04 |
| 41 | …. The function sends → ? | `␣a` | 0.329 | 1 | `␣a` 0.33, `␣the` 0.24, `␣an` 0.13, `␣its` 0.04, `␣out` 0.04 |
| 42 | …The function sends a → ? | `␣value` | 0.048 | 5 | `␣message` 0.19, `␣request` 0.06, `␣response` 0.05, `␣string` 0.05, `␣value` 0.05 |
| 43 | …function sends a value → ? | `␣back` | 0.013 | 4 | `␣to` 0.80, `,` 0.02, `␣(` 0.01, `␣back` 0.01, `␣of` 0.01 |
| 44 | …sends a value back → ? | `␣to` | 0.909 | 1 | `␣to` 0.91, `␣when` 0.01, `,` 0.01, `␣as` 0.01, `␣every` 0.01 |
| 45 | …a value back to → ? | `␣the` | 0.867 | 1 | `␣the` 0.87, `␣its` 0.07, `␣a` 0.02, `␣an` 0.01, `␣Python` 0.00 |
| 46 | …value back to the → ? | `␣call` | 0.062 | 4 | `␣console` 0.12, `␣user` 0.10, `␣calling` 0.07, `␣call` 0.06, `␣parent` 0.05 |
| 47 | …back to the call → ? | `er` | 0.979 | 1 | `er` 0.98, `back` 0.02, `␣stack` 0.00, `ers` 0.00, `␣center` 0.00 |
| 48 | …to the caller → ? | `␣using` | 0.022 | 13 | `,` 0.19, `.` 0.15, `.\n` 0.07, `␣when` 0.06, `␣as` 0.04 |
| 49 | …the caller using → ? | `␣the` | 0.742 | 1 | `␣the` 0.74, `␣a` 0.08, `␣its` 0.03, `␣return` 0.02, `␣an` 0.01 |
| 50 | …caller using the → ? | `␣return` | 0.256 | 1 | `␣return` 0.26, `␣def` 0.13, `␣get` 0.02, `␣function` 0.02, `␣arguments` 0.02 |
| 51 | …er using the return → ? | `␣statement` | 0.253 | 3 | `␣value` 0.34, `␣keyword` 0.27, `␣statement` 0.25, `␣type` 0.03, `_` 0.01 |
| 52 | …using the return statement → ? | `.` | 0.405 | 1 | `.` 0.41, `.\n` 0.23, `,` 0.11, `.\n\n` 0.06, `␣and` 0.02 |

**Previous-token predictions (backward model, read right to left)**

| Step | ? ← Right context | True token | p(true) | Rank | Top-5 predictions |
|---:|---|---|---:|---:|---|
| 1 | ? ← [end of text] | `.` | 0.519 | 1 | `.` 0.52, `!` 0.03, `)` 0.02, `).` 0.01, `?` 0.01 |
| 2 | ? ← . | `␣statement` | 0.000 | 870 | `␣it` 0.01, `␣time` 0.01, `␣them` 0.00, `␣Yes` 0.00, `␣years` 0.00 |
| 3 | ? ← statement. | `␣return` | 0.001 | 83 | `␣a` 0.16, `␣this` 0.10, `␣the` 0.07, `␣fashion` 0.04, `␣mission` 0.03 |
| 4 | ? ← return statement. | `␣the` | 0.336 | 1 | `␣the` 0.34, `␣a` 0.25, `␣your` 0.02, `'s` 0.02, `␣or` 0.02 |
| 5 | ? ← the return statement. | `␣using` | 0.009 | 16 | `␣in` 0.38, `␣of` 0.10, `␣after` 0.06, `␣to` 0.06, `␣before` 0.04 |
| 6 | ? ← using the return statement… | `er` | 0.001 | 135 | `␣by` 0.07, `,` 0.06, `␣By` 0.03, `␣it` 0.03, `␣or` 0.02 |
| 7 | ? ← er using the return… | `␣call` | 0.344 | 1 | `␣call` 0.34, `␣pars` 0.24, `␣Integ` 0.06, `ugg` 0.05, `␣lex` 0.02 |
| 8 | ? ← caller using the… | `␣the` | 0.847 | 1 | `␣the` 0.85, `␣a` 0.03, `␣function` 0.01, `␣The` 0.01, `␣your` 0.01 |
| 9 | ? ← the caller using… | `␣to` | 0.341 | 1 | `␣to` 0.34, `␣by` 0.13, `␣of` 0.11, `␣from` 0.07, `␣for` 0.03 |
| 10 | ? ← to the caller… | `␣back` | 0.143 | 2 | `␣returned` 0.20, `␣back` 0.14, `␣it` 0.06, `␣return` 0.06, `␣returns` 0.03 |
| 11 | ? ← back to the call… | `␣value` | 0.021 | 12 | `␣it` 0.13, `␣returned` 0.06, `␣data` 0.05, `␣return` 0.04, `␣result` 0.03 |
| 12 | ? ← value back to the… | `␣a` | 0.026 | 5 | `␣return` 0.25, `␣the` 0.24, `␣returned` 0.11, `␣its` 0.03, `␣a` 0.03 |
| 13 | ? ← a value back to… | `␣sends` | 0.051 | 5 | `␣return` 0.30, `␣returns` 0.14, `␣pass` 0.07, `␣returning` 0.06, `␣sends` 0.05 |
| 14 | ? ← sends a value back… | `␣function` | 0.080 | 4 | `␣and` 0.30, `␣It` 0.21, `␣then` 0.09, `␣function` 0.08, `␣it` 0.04 |
| 15 | ? ← function sends a value… | `␣The` | 0.075 | 4 | `()` 0.18, `'` 0.16, `back` 0.09, `␣The` 0.07, `␣the` 0.07 |
| 16 | ? ← The function sends a… | `.` | 0.059 | 2 | `:` 0.93, `.` 0.06, `).` 0.00, `)` 0.00, `."` 0.00 |
| 17 | ? ← . The function sends… | `␣definition` | 0.000 | 342 | `␣False` 0.11, `␣function` 0.10, `␣value` 0.05, `er` 0.03, `␣statement` 0.03 |
| 18 | ? ← definition. The function… | `␣the` | 0.083 | 2 | `␣function` 0.37, `␣return` 0.08, `␣the` 0.08, `␣its` 0.05, `␣class` 0.02 |
| 19 | ? ← the definition. The… | `␣below` | 0.001 | 82 | `␣in` 0.23, `␣of` 0.18, `␣to` 0.11, `␣from` 0.06, `␣on` 0.05 |
| 20 | ? ← below the definition.… | `ented` | 0.000 | 458 | `␣statement` 0.09, `␣code` 0.04, `␣function` 0.04, `␣just` 0.04, `␣directly` 0.04 |
| 21 | ? ← ented below the definition… | `␣ind` | 0.954 | 1 | `␣ind` 0.95, `␣Ind` 0.01, `␣acc` 0.01, `res` 0.01, `ind` 0.00 |
| 22 | ? ← indented below the… | `␣is` | 0.326 | 1 | `␣is` 0.33, `␣are` 0.10, `␣be` 0.10, `,` 0.06, `␣statement` 0.03 |
| 23 | ? ← is indented below… | `␣function` | 0.063 | 5 | `␣value` 0.11, `␣statement` 0.11, `␣which` 0.08, `␣that` 0.07, `␣function` 0.06 |
| 24 | ? ← function is indented… | `␣the` | 0.596 | 1 | `␣the` 0.60, `␣a` 0.11, `␣The` 0.07, `␣return` 0.03, `␣calling` 0.01 |
| 25 | ? ← the function is ind… | `␣of` | 0.481 | 1 | `␣of` 0.48, `␣to` 0.06, `␣for` 0.06, `␣in` 0.05, `,` 0.05 |
| 26 | ? ← of the function is… | `␣body` | 0.112 | 2 | `␣name` 0.35, `␣body` 0.11, `␣statement` 0.07, `␣value` 0.07, `␣argument` 0.04 |
| 27 | ? ← body of the function… | `␣the` | 0.252 | 2 | `␣The` 0.65, `␣the` 0.25, `The` 0.05, `␣main` 0.01, `␣return` 0.01 |
| 28 | ? ← the body of the… | `␣and` | 0.129 | 3 | `,` 0.25, `␣in` 0.15, `␣and` 0.13, `␣that` 0.13, `␣of` 0.04 |
| 29 | ? ← and the body of… | `,` | 0.615 | 1 | `,` 0.62, `␣statement` 0.05, `␣function` 0.03, `),` 0.01, `␣definition` 0.01 |
| 30 | ? ← , and the body… | `heses` | 0.007 | 22 | `␣statement` 0.12, `␣function` 0.10, `␣definition` 0.04, `␣value` 0.03, `er` 0.02 |
| 31 | ? ← heses, and the… | `␣parent` | 0.998 | 1 | `␣parent` 1.00, `␣Parent` 0.00, `parent` 0.00, `Parent` 0.00, `t` 0.00 |
| 32 | ? ← parentheses, and… | `␣in` | 0.547 | 1 | `␣in` 0.55, `␣by` 0.10, `␣inside` 0.06, `␣of` 0.06, `␣the` 0.05 |
| 33 | ? ← in parentheses,… | `␣listed` | 0.001 | 63 | `␣enclosed` 0.39, `␣given` 0.06, `␣is` 0.04, `␣defined` 0.04, `␣written` 0.03 |
| 34 | ? ← listed in parentheses… | `␣are` | 0.544 | 1 | `␣are` 0.54, `␣is` 0.32, `␣not` 0.01, `␣be` 0.01, `␣function` 0.01 |
| 35 | ? ← are listed in parent… | `␣parameters` | 0.040 | 5 | `␣arguments` 0.14, `␣values` 0.09, `␣functions` 0.09, `␣function` 0.09, `␣parameters` 0.04 |
| 36 | ? ← parameters are listed in… | `␣The` | 0.236 | 1 | `␣The` 0.24, `␣function` 0.10, `␣the` 0.07, `'s` 0.05, `␣All` 0.04 |
| 37 | ? ← The parameters are listed… | `.` | 0.814 | 1 | `.` 0.81, `:` 0.13, `).` 0.02, `".` 0.01, `."` 0.00 |
| 38 | ? ← . The parameters are… | `␣name` | 0.014 | 10 | `␣function` 0.17, `␣statement` 0.05, `␣parameters` 0.03, `␣value` 0.03, `␣functions` 0.03 |
| 39 | ? ← name. The parameters… | `␣its` | 0.062 | 2 | `␣function` 0.49, `␣its` 0.06, `'s` 0.06, `␣the` 0.05, `␣a` 0.04 |
| 40 | ? ← its name. The… | `␣by` | 0.176 | 1 | `␣by` 0.18, `␣in` 0.11, `␣of` 0.09, `␣to` 0.08, `␣after` 0.05 |
| 41 | ? ← by its name.… | `␣followed` | 0.313 | 1 | `␣followed` 0.31, `␣function` 0.13, `␣specified` 0.07, `␣called` 0.06, `␣defined` 0.06 |
| 42 | ? ← followed by its name… | `␣keyword` | 0.014 | 9 | `,` 0.41, `␣function` 0.08, `␣name` 0.06, `"` 0.03, `␣statement` 0.02 |
| 43 | ? ← keyword followed by its… | `␣def` | 0.001 | 63 | `␣the` 0.37, `␣a` 0.31, `␣function` 0.06, `␣or` 0.02, `␣return` 0.02 |
| 44 | ? ← def keyword followed by… | `␣the` | 0.930 | 1 | `␣the` 0.93, `␣a` 0.02, `␣or` 0.01, `␣with` 0.00, `␣using` 0.00 |
| 45 | ? ← the def keyword followed… | `␣using` | 0.364 | 1 | `␣using` 0.36, `␣with` 0.24, `␣by` 0.09, `␣of` 0.06, `␣uses` 0.05 |
| 46 | ? ← using the def keyword… | `␣defined` | 0.160 | 1 | `␣defined` 0.16, `␣function` 0.16, `␣by` 0.16, `␣called` 0.06, `␣named` 0.04 |
| 47 | ? ← defined using the def… | `␣is` | 0.932 | 1 | `␣is` 0.93, `␣be` 0.03, `␣function` 0.01, `␣typically` 0.00, `␣are` 0.00 |
| 48 | ? ← is defined using the… | `␣function` | 0.714 | 1 | `␣function` 0.71, `␣It` 0.03, `␣Function` 0.02, `␣that` 0.02, `␣statement` 0.01 |
| 49 | ? ← function is defined using… | `␣a` | 0.037 | 7 | `␣The` 0.20, `The` 0.12, `␣A` 0.09, `A` 0.09, `()` 0.05 |
| 50 | ? ← a function is defined… | `,` | 0.665 | 1 | `,` 0.66, `␣of` 0.16, `␣for` 0.02, `␣that` 0.02, `␣in` 0.01 |
| 51 | ? ← , a function is… | `␣Python` | 0.127 | 1 | `␣Python` 0.13, `␣Java` 0.08, `␣example` 0.08, `␣function` 0.03, `++` 0.03 |
| 52 | ? ← Python, a function… | `In` | 0.542 | 1 | `In` 0.54, `␣In` 0.39, `␣in` 0.06, `␣of` 0.00, `.In` 0.00 |
