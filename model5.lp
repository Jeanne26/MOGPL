\ Model model5
\ LP format - for model browsing. Use MPS format to capture full model detail.
Maximize
  5 r5 - b15 - b25 - b35 - b45 - b55 - b65
Subject To
 R0: r5 - b15 <= 2
 R1: r5 - b25 <= 9
 R2: r5 - b35 <= 6
 R3: r5 - b45 <= 8
 R4: r5 - b55 <= 5
 R5: r5 - b65 <= 4
Bounds
End
