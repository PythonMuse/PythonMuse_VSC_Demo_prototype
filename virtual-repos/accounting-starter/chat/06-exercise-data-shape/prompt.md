---
title: Exercise · What breaks if the export changes shape?
---
Next year someone exports the 2026 trial balance from QuickBooks, and the first column reads `1000 · Checking` instead of an account code. What breaks?

Test it on account codes and names only, with no amounts. Cover three cases: joining on that column as it is, splitting the code from the name, and comparing by row position when 2026 gains one new account inserted mid-list (say 6095 Software - AI tools). Say what the script should do about each.
