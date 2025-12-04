# Plan: Documentation Completion

## Goal
Complete documentation with 4 new compact pages (English, no code examples).

## New Files Created

### 1. `docs/configuration/settings_reference.md` - Settings Reference
Compact parameter tables, NO code. Structure:
- Apple VAS (VAS#MerchantID, VAS#KeySlot, VAS#MerchantURL)
- Google Smart Tap (ST#CollectorID, ST#KeySlot, ST#KeyVersion)
- Keyboard (KBLogMode, KBSource, KBEnable, KBPrefix, KBPostfix, KBDelayMS, KBPass*)
- NFC Tags (NFCType2/4/5, TagRead*, IgnoreRandomUID, TagByteOrder)
- DESFire (DESFire#AppID, #FileID, #KeyNum, #KeySlot, #Crypto, #Format, etc.)
- LED (LEDMode, LEDSelect, PassLED, TagLED, PassErrorLED, StartLED)
- Beep (PassBeep, TagBeep, PassErrorBeep, StartBeep)

Format per section: Parameter | Type | Range | Default | Description

### 2. `docs/references/cli.md` - CLI Reference
All commands with options:
- `vtap100 generate` - all flags
- `vtap100 wizard` - usage
- `vtap100 editor` - usage
- `vtap100 validate` - usage
- `vtap100 docs` - usage

### 3. `docs/wizard.md` - Wizard Guide
Step-by-step walkthrough of interactive wizard screens.

### 4. `docs/troubleshooting.md` - FAQ & Troubleshooting
Consolidate from existing docs + common issues:
- Reader not recognized
- Config not applied
- Key errors
- Common mistakes

## Files Updated

### `docs/README.md`
Added to Table of Contents:
- Reference section: Settings Reference, CLI Reference
- Getting Started: Wizard Guide
- New section: Troubleshooting

## Implementation Order

1. ✅ Settings Reference (main request)
2. ✅ CLI Reference
3. ✅ Wizard Guide
4. ✅ Troubleshooting
5. ✅ Update README.md
6. ✅ Copy plan to `docs/PLAN_DOCUMENTATION.md`

## Files Modified

| File | Action | Status |
|------|--------|--------|
| `docs/configuration/settings_reference.md` | CREATE | ✅ |
| `docs/references/cli.md` | CREATE | ✅ |
| `docs/wizard.md` | CREATE | ✅ |
| `docs/troubleshooting.md` | CREATE | ✅ |
| `docs/README.md` | UPDATE | ✅ |
| `docs/PLAN_DOCUMENTATION.md` | CREATE | ✅ |
