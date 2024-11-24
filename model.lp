\ Model MinMaxRegret
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  t
Subject To
 R0: 70 x1 + 18 x2 + 16 x3 + 14 x4 + 12 x5 + 10 x6 + 8 x7 + 6 x8 + 4 x9
   + 2 x10 + t >= 112
 R1: 2 x1 + 4 x2 + 6 x3 + 8 x4 + 10 x5 + 12 x6 + 14 x7 + 16 x8 + 18 x9
   + 70 x10 + t >= 118
 R2: 60 x1 + 10 x2 + 15 x3 + 20 x4 + 25 x5 + 20 x6 + 5 x7 + 15 x8 + 20 x9
   + 60 x10 <= 100
Bounds
Binaries
 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10
End
