from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else "upstream")

validate_path = root / "src/settings/validate.cpp"
validate = validate_path.read_text(encoding="utf-8")

setup_only_pattern = re.compile(
    r"const char\* SettingsPatch::setupOnlyStep\(\) const \{.*?\n\}",
    re.DOTALL,
)
setup_only_replacement = '''const char* SettingsPatch::setupOnlyStep() const {
  if (rgbOrder != nullptr) {
    return "rgb";
  }

  return nullptr;
}'''

validate, count = setup_only_pattern.subn(setup_only_replacement, validate, count=1)
if count != 1:
    raise SystemExit("Could not patch SettingsPatch::setupOnlyStep()")
validate_path.write_text(validate, encoding="utf-8")

config_path = root / "ui/src/config/ConfigForm.tsx"
config = config_path.read_text(encoding="utf-8")

marker = 'const EYES_STYLES = ["classic", "kaomoji", "cover", "dots"];\n'
servo_names = 'const SERVO_NAMES = ["Head", "Neck", "Hand left", "Hand right", "Body"] as const;'
if servo_names not in config:
    if marker not in config:
        raise SystemExit("Could not locate EYES_STYLES")
    config = config.replace(marker, marker + "\n" + servo_names + "\n", 1)

old_draft = '''    loading: settings.loading,
    eyesStyle: settings.eyes_style,
  };'''
new_draft = '''    loading: settings.loading,
    eyesStyle: settings.eyes_style,
    servoMins: [...settings.servo_mins],
    servoMaxs: [...settings.servo_maxs],
    oledRotate180: settings.oled_rotate_180,
  };'''
if old_draft not in config:
    raise SystemExit("Could not patch draftFrom()")
config = config.replace(old_draft, new_draft, 1)

old_set = '''  const set = (fields: Partial<typeof draft>) =>
    setDraft((previous) => ({ ...previous, ...fields }));
'''
new_set = '''  const set = (fields: Partial<typeof draft>) =>
    setDraft((previous) => ({ ...previous, ...fields }));

  const setServoMin = (index: number, value: number) => {
    const servoMins = [...draft.servoMins];
    const current = servoMins[index];
    const maxAllowed = Math.max(0, draft.servoMaxs[index] - 1);
    servoMins[index] = Number.isNaN(value) ? current : Math.round(clamp(value, 0, maxAllowed));
    set({ servoMins });
  };

  const setServoMax = (index: number, value: number) => {
    const servoMaxs = [...draft.servoMaxs];
    const current = servoMaxs[index];
    const minAllowed = Math.min(180, draft.servoMins[index] + 1);
    servoMaxs[index] = Number.isNaN(value) ? current : Math.round(clamp(value, minAllowed, 180));
    set({ servoMaxs });
  };
'''
if old_set not in config:
    raise SystemExit("Could not add servo limit setters")
config = config.replace(old_set, new_set, 1)

old_json = '''          loading: draft.loading,
          eyes_style: draft.eyesStyle,
          ...(newToken === undefined ? {} : { access_token: newToken }),'''
new_json = '''          loading: draft.loading,
          eyes_style: draft.eyesStyle,
          servo_mins: draft.servoMins,
          servo_maxs: draft.servoMaxs,
          oled_rotate_180: draft.oledRotate180,
          ...(newToken === undefined ? {} : { access_token: newToken }),'''
if old_json not in config:
    raise SystemExit("Could not patch save payload")
config = config.replace(old_json, new_json, 1)

ui_marker = '      <ConfigSection title="Display" head>\n'
if ui_marker not in config:
    raise SystemExit("Could not locate Display section")

servo_ui = '''      <ConfigSection title="Servo limits" apply="now">
        <p className="config-section-desc">
          These limits clamp every animation. Start conservatively and increase the range only after
          checking that the mechanism does not hit a physical stop.
        </p>
        {SERVO_NAMES.map((name, index) => (
          <div className="form-group" key={name}>
            <label>{name}</label>
            <div className="range-row">
              <input
                type="number"
                aria-label={`${name} minimum angle`}
                min="0"
                max={Math.max(0, draft.servoMaxs[index] - 1)}
                step="1"
                required
                value={draft.servoMins[index]}
                onInput={(event) => setServoMin(index, event.currentTarget.valueAsNumber)}
              />
              <input
                type="number"
                aria-label={`${name} maximum angle`}
                min={Math.min(180, draft.servoMins[index] + 1)}
                max="180"
                step="1"
                required
                value={draft.servoMaxs[index]}
                onInput={(event) => setServoMax(index, event.currentTarget.valueAsNumber)}
              />
            </div>
            <p className="hint">Minimum / maximum angle in degrees</p>
          </div>
        ))}
      </ConfigSection>
      <ConfigSection title="OLED orientation" apply="now">
        <div className="form-group">
          <div className="toggle-row">
            <input
              type="checkbox"
              id="config-oled-rotate"
              checked={draft.oledRotate180}
              onChange={(event) => set({ oledRotate180: event.currentTarget.checked })}
            />
            <label htmlFor="config-oled-rotate">Rotate OLED 180°</label>
          </div>
        </div>
      </ConfigSection>
'''

if 'title="Servo limits"' not in config:
    config = config.replace(ui_marker, servo_ui + ui_marker, 1)

config_path.write_text(config, encoding="utf-8")

validate_check = validate_path.read_text(encoding="utf-8")
config_check = config_path.read_text(encoding="utf-8")

for forbidden in ['return "servo";', 'return "oled";']:
    if forbidden in validate_check:
        raise SystemExit(f"Backend verification failed: {forbidden}")

for required in [
    'title="Servo limits"',
    'servo_mins: draft.servoMins',
    'servo_maxs: draft.servoMaxs',
    'oled_rotate_180: draft.oledRotate180',
    'Rotate OLED 180°',
]:
    if required not in config_check:
        raise SystemExit(f"UI verification failed: {required}")

print("Runtime servo limits and OLED rotation enabled in /config")
