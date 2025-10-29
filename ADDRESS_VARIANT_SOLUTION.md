# Address Variant Generation Enhancement

## Problem
The original `generate_variant` function had limited pattern matching that couldn't handle various address input formats commonly found in Singapore addresses, including:
- Comma-separated formats: `"61 ALIWAL STREET #01-01, 199937"`
- Block suffixes: `"109C AMOY STREET #04-00, 069929"`
- Spacing variations in unit and block notation
- Missing postal codes
- Various postal code formats

## Solution

### 1. Added `normalize_address_format()` Function
A preprocessing function that standardizes address formats before variant generation:

```python
def normalize_address_format(address):
    """
    Normalize address format by cleaning up common variations.
    Handles commas, extra spaces, and standardizes formatting.
    """
```

**Features:**
- Removes multiple commas and converts to spaces
- Normalizes multiple spaces to single space
- Standardizes unit notation spacing (`#01-01`)
- Fixes postal code formats (`Singapore123456` → `Singapore 123456`)
- Handles various input data types and edge cases

### 2. Enhanced `generate_variant()` Function
Completely rewrote the pattern matching to handle diverse address formats:

**New Patterns Supported:**

1. **Unit to Suffix Conversion:**
   - `"61 ALIWAL STREET #01-01, 199937"` → `"61 ALIWAL STREET 199937"`
   - `"25 BOAT QUAY #02-03"` → `"25A BOAT QUAY"`
   - `"109C AMOY STREET #04-00"` → `"109C AMOY STREET"` (preserves existing block suffix)

2. **Suffix to Unit Conversion:**
   - `"61A ALIWAL STREET 199937"` → `"61 ALIWAL STREET #02-01 199937"`
   - `"61 A ALIWAL STREET 199937"` → `"61 ALIWAL STREET #02-01 199937"` (handles spaces)

3. **Block Suffix Handling:**
   - Recognizes when blocks already have suffixes (e.g., "109C")
   - Preserves existing suffixes instead of trying to convert them

4. **Flexible Floor Mapping:**
   - `#01` → `""` (no suffix)
   - `#02` → `A`
   - `#03` → `B`
   - `#04` → `C`
   - `#05` → `D`
   - Supports floors beyond #05 (extended from original #01-#05 limit)

### 3. Updated Integration
Modified the main processing flow to use normalization before variant generation:

```python
# For shophouse, try to generate an address format variant
# First normalize the address format to handle commas, spacing, etc.
normalized_address = normalize_address_format(clean_address)
variant_address = generate_variant(normalized_address)
```

## Test Results

The enhanced solution successfully handles all the problem cases:

| Input | Normalized | Generated Variant |
|-------|------------|-------------------|
| `"61 ALIWAL STREET #01-01, 199937"` | `"61 ALIWAL STREET #01-01 199937"` | `"61 ALIWAL STREET 199937"` |
| `"109C AMOY STREET #04-00, 069929"` | `"109C AMOY STREET #04-00 069929"` | `"109C AMOY STREET 069929"` |
| `"61   A    ALIWAL STREET   ,   199937"` | `"61 A ALIWAL STREET 199937"` | `"61 ALIWAL STREET #02-01 199937"` |
| `"25,BOAT QUAY,#02-03,049958"` | `"25 BOAT QUAY #02-03 049958"` | `"25A BOAT QUAY 049958"` |

## Benefits

1. **Improved Search Accuracy:** Generates more accurate variants for different address formats
2. **Better Coverage:** Handles comma-separated addresses, block suffixes, and spacing variations
3. **Robust Processing:** Normalizes inputs before processing to reduce parsing failures
4. **Bidirectional Conversion:** Converts both ways (unit↔suffix) for maximum search coverage
5. **Fallback Mechanism:** Uses normalized address when variant generation isn't possible

## Implementation

The changes are implemented in `/workspaces/SCOUT/enforcement_engine.py`:
- Added `normalize_address_format()` function (lines ~223-250)
- Enhanced `generate_variant()` function (lines ~253-330)
- Updated integration in `process_single_address()` (lines ~575-585)

## Impact

Line 548 (and surrounding lines) now calls the enhanced `generate_variant` function with proper normalization, ensuring that address searches consider accurate variants regardless of input format variations, leading to more reliable occupant identification and compliance assessment.