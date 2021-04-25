# Guide to Backend functions

## Histogram
Args:
1. string: Absolute path to location of CSV
2. string: Column on which to create the histogram
Returns:
1. Return value of get_img function

## Rename columns
Args:
1. string: Absolute path to location of CSV
2. string: Old column name (the one that's being changed)
3. string: New column name
Returns:
None

## Drop Columns
Args:
1. string: Absolute path to location of CSV
2. list of strings: list of columns to drop (by name)
Returns:
None

## Linear Regression
Args:
1. string: Absolute path to location of CSV
Returns:
1. dictionary: Dict of all coefficients for regression
  - Should be keyed on column name (string)
  - Value should be coefficient value (float)

I think that's it. If there's any questions, let Owen know. 
