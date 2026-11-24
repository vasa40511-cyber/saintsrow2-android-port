#!/usr/bin/env python3
from pathlib import Path

ROOT = Path("app/src/main/java")

def replace_once(path, old, new):
    p = ROOT / path
    s = p.read_text(encoding="utf-8")
    count = s.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one patch anchor, found {count}: {old[:90]!r}")
    p.write_text(s.replace(old, new, 1), encoding="utf-8")

vk_path = "javax/microedition/lcdui/keyboard/VirtualKeyboard.java"
replace_once(vk_path,
    "\tprivate static final int TYPE_ARROWS = 6;\n",
    "\tprivate static final int TYPE_ARROWS = 6;\n\tprivate static final int TYPE_SAINTS_ROW = 7;\n")

replace_once(vk_path,
    "\tprivate int layoutVariant;\n",
    """\tprivate int layoutVariant;
\tprivate int joystickPointer = -1;
\tprivate float joystickCenterX;
\tprivate float joystickCenterY;
\tprivate float joystickRadius;
\tprivate float joystickKnobX;
\tprivate float joystickKnobY;
\tprivate int joystickHorizontal;
\tprivate int joystickVertical;
""")

replace_once(vk_path,
    """\t\t\t\tsetSnap(KEY_MENU, SCREEN, RectSnap.INT_NORTHEAST, false);
\t\t\t\tbreak;
\t\t}
\t}

\tpublic int getLayout() {""",
    """\t\t\t\tsetSnap(KEY_MENU, SCREEN, RectSnap.INT_NORTHEAST, false);
\t\t\t\tbreak;
\t\t\tcase TYPE_SAINTS_ROW:
\t\t\t\tArrays.fill(keyScales, 1.0f);
\t\t\t\tfor (VirtualKey key : keypad) {
\t\t\t\t\tkey.visible = false;
\t\t\t\t\tkey.snapOrigin = SCREEN;
\t\t\t\t\tkey.snapMode = RectSnap.NO_SNAP;
\t\t\t\t\tkey.snapValid = false;
\t\t\t\t}
\t\t\t\tsetSnap(KEY_A, SCREEN, RectSnap.INT_NORTHEAST, true);
\t\t\t\tsetSnap(KEY_B, SCREEN, RectSnap.INT_EAST, true);
\t\t\t\tsetSnap(KEY_C, SCREEN, RectSnap.INT_SOUTHEAST, true);
\t\t\t\tsetSnap(KEY_D, SCREEN, RectSnap.INT_SOUTH, true);
\t\t\t\tbreak;
\t\t}
\t}

\tpublic int getLayout() {""")

replace_once(vk_path,
    """\t\tboolean opaque = !obscuresVirtualScreen || settings.vkForceOpacity;
\t\tfor (VirtualKey key : keypad) {
\t\t\tkey.opaque &= opaque;
\t\t}
\t}

\tpublic boolean isPhone() {""",
    """\t\tif (layoutVariant == TYPE_SAINTS_ROW) {
\t\t\tfloat h = screen.height();
\t\t\tfloat buttonSize = Math.min(keySize * 0.88f, h * 0.17f);
\t\t\tfloat spread = buttonSize * 1.15f;
\t\t\tfloat actionX = screen.right - buttonSize * 1.75f;
\t\t\tfloat actionY = screen.centerY();
\t\t\tplaceKey(KEY_A, actionX, actionY - spread, buttonSize);
\t\t\tplaceKey(KEY_B, actionX + spread, actionY, buttonSize);
\t\t\tplaceKey(KEY_C, actionX, actionY + spread, buttonSize);
\t\t\tplaceKey(KEY_D, actionX - spread, actionY, buttonSize);

\t\t\tjoystickCenterX = screen.left + h * 0.20f;
\t\t\tjoystickCenterY = screen.centerY();
\t\t\tjoystickRadius = h * 0.16f;
\t\t\tjoystickKnobX = joystickCenterX;
\t\t\tjoystickKnobY = joystickCenterY;
\t\t\tobscuresVirtualScreen = false;
\t\t\tfor (VirtualKey key : keypad) {
\t\t\t\tkey.opaque = false;
\t\t\t}
\t\t\treturn;
\t\t}
\t\tboolean opaque = !obscuresVirtualScreen || settings.vkForceOpacity;
\t\tfor (VirtualKey key : keypad) {
\t\t\tkey.opaque &= opaque;
\t\t}
\t}

\tprivate void placeKey(int index, float centerX, float centerY, float size) {
\t\tVirtualKey key = keypad[index];
\t\tkey.rect.set(centerX - size / 2, centerY - size / 2,
\t\t\t\tcenterX + size / 2, centerY + size / 2);
\t\tkey.corners = (int) (size * 0.25f);
\t\tkey.snapValid = true;
\t}

\tpublic boolean isPhone() {""")

replace_once(vk_path,
    """\t\t\tfor (VirtualKey key : keypad) {
\t\t\t\tif (key.visible) {
\t\t\t\t\tkey.paint(g);
\t\t\t\t}
\t\t\t}
\t\t}
\t}

\t@Override
\tpublic boolean pointerPressed(int pointer, float x, float y) {
\t\tswitch (layoutEditMode) {""",
    """\t\t\tfor (VirtualKey key : keypad) {
\t\t\t\tif (key.visible) {
\t\t\t\t\tkey.paint(g);
\t\t\t\t}
\t\t\t}
\t\t\tif (layoutVariant == TYPE_SAINTS_ROW) {
\t\t\t\tpaintJoystick(g);
\t\t\t}
\t\t}
\t}

\tprivate void paintJoystick(CanvasWrapper g) {
\t\tRectF base = new RectF(joystickCenterX - joystickRadius,
\t\t\t\tjoystickCenterY - joystickRadius,
\t\t\t\tjoystickCenterX + joystickRadius,
\t\t\t\tjoystickCenterY + joystickRadius);
\t\tg.setFillColor(0x55202A35);
\t\tg.fillArc(base, 0, 360);
\t\tg.setDrawColor(0x99E8F0F7);
\t\tg.drawArc(base, 0, 360);
\t\tRectF inner = new RectF(joystickCenterX - joystickRadius * 0.58f,
\t\t\t\tjoystickCenterY - joystickRadius * 0.58f,
\t\t\t\tjoystickCenterX + joystickRadius * 0.58f,
\t\t\t\tjoystickCenterY + joystickRadius * 0.58f);
\t\tg.setDrawColor(0x44FFFFFF);
\t\tg.drawArc(inner, 0, 360);
\t\tfloat knobRadius = joystickRadius * 0.38f;
\t\tRectF knob = new RectF(joystickKnobX - knobRadius, joystickKnobY - knobRadius,
\t\t\t\tjoystickKnobX + knobRadius, joystickKnobY + knobRadius);
\t\tg.setFillColor(0xAA20AFC3);
\t\tg.fillArc(knob, 0, 360);
\t\tg.setDrawColor(0xDDFFFFFF);
\t\tg.drawArc(knob, 0, 360);
\t}

\t@Override
\tpublic boolean pointerPressed(int pointer, float x, float y) {
\t\tif (layoutVariant == TYPE_SAINTS_ROW && layoutEditMode == LAYOUT_EOF
\t\t\t\t&& joystickPointer == -1 && isJoystickHit(x, y)) {
\t\t\tjoystickPointer = pointer;
\t\t\tupdateJoystick(x, y);
\t\t\toverlayView.postInvalidate();
\t\t\treturn true;
\t\t}
\t\tswitch (layoutEditMode) {""")

replace_once(vk_path,
    """\t@Override
\tpublic boolean pointerDragged(int pointer, float x, float y) {
\t\tswitch (layoutEditMode) {""",
    """\tpublic boolean pointerDragged(int pointer, float x, float y) {
\t\tif (layoutVariant == TYPE_SAINTS_ROW && pointer == joystickPointer) {
\t\t\tupdateJoystick(x, y);
\t\t\toverlayView.postInvalidate();
\t\t\treturn true;
\t\t}
\t\tswitch (layoutEditMode) {""")

replace_once(vk_path,
    """\t@Override
\tpublic boolean pointerReleased(int pointer, float x, float y) {
\t\tif (layoutEditMode == LAYOUT_EOF) {""",
    """\t@Override
\tpublic boolean pointerReleased(int pointer, float x, float y) {
\t\tif (layoutVariant == TYPE_SAINTS_ROW && pointer == joystickPointer) {
\t\t\treleaseJoystick();
\t\t\tjoystickPointer = -1;
\t\t\toverlayView.postInvalidate();
\t\t\treturn true;
\t\t}
\t\tif (layoutEditMode == LAYOUT_EOF) {""")

replace_once(vk_path,
    """\t@Override
\tpublic void cancel() {
\t\tfor (VirtualKey key : keypad) {
\t\t\tkey.selected = false;
\t\t\thandler.removeCallbacks(key);
\t\t}
\t}""",
    """\t@Override
\tpublic void cancel() {
\t\treleaseJoystick();
\t\tjoystickPointer = -1;
\t\tfor (int i = 0; i < associatedKeys.length; i++) {
\t\t\tVirtualKey key = associatedKeys[i];
\t\t\tif (key != null) {
\t\t\t\tassociatedKeys[i] = null;
\t\t\t\tif (target != null) {
\t\t\t\t\tkey.onUp();
\t\t\t\t} else {
\t\t\t\t\tkey.selected = false;
\t\t\t\t\thandler.removeCallbacks(key);
\t\t\t\t}
\t\t\t}
\t\t}
\t\tfor (VirtualKey key : keypad) {
\t\t\tkey.selected = false;
\t\t\thandler.removeCallbacks(key);
\t\t}
\t}""")

replace_once(vk_path,
    """\tpublic void show() {
\t\tif (settings.vkHideDelay > 0 && obscuresVirtualScreen) {""",
    """\tprivate boolean isJoystickHit(float x, float y) {
\t\tfloat dx = x - joystickCenterX;
\t\tfloat dy = y - joystickCenterY;
\t\tfloat hitRadius = joystickRadius * 1.55f;
\t\treturn dx * dx + dy * dy <= hitRadius * hitRadius;
\t}

\tprivate void updateJoystick(float x, float y) {
\t\tfloat dx = x - joystickCenterX;
\t\tfloat dy = y - joystickCenterY;
\t\tfloat distance = (float) Math.hypot(dx, dy);
\t\tif (distance > joystickRadius && distance > 0) {
\t\t\tfloat scale = joystickRadius / distance;
\t\t\tdx *= scale;
\t\t\tdy *= scale;
\t\t\tdistance = joystickRadius;
\t\t}
\t\tjoystickKnobX = joystickCenterX + dx;
\t\tjoystickKnobY = joystickCenterY + dy;

\t\tint nextHorizontal = 0;
\t\tint nextVertical = 0;
\t\tif (distance > joystickRadius * 0.22f) {
\t\t\tif (Math.abs(dx) > Math.abs(dy) * 0.55f) {
\t\t\t\tnextHorizontal = dx < 0 ? -1 : 1;
\t\t\t}
\t\t\tif (Math.abs(dy) > Math.abs(dx) * 0.55f) {
\t\t\t\tnextVertical = dy < 0 ? -1 : 1;
\t\t\t}
\t\t}
\t\tif (nextHorizontal != joystickHorizontal) {
\t\t\tif (joystickHorizontal != 0 && target != null) {
\t\t\t\ttarget.postKeyReleased(joystickHorizontal < 0 ? Canvas.KEY_LEFT : Canvas.KEY_RIGHT);
\t\t\t}
\t\t\tif (nextHorizontal != 0 && target != null) {
\t\t\t\ttarget.postKeyPressed(nextHorizontal < 0 ? Canvas.KEY_LEFT : Canvas.KEY_RIGHT);
\t\t\t}
\t\t\tjoystickHorizontal = nextHorizontal;
\t\t}
\t\tif (nextVertical != joystickVertical) {
\t\t\tif (joystickVertical != 0 && target != null) {
\t\t\t\ttarget.postKeyReleased(joystickVertical < 0 ? Canvas.KEY_UP : Canvas.KEY_DOWN);
\t\t\t}
\t\t\tif (nextVertical != 0 && target != null) {
\t\t\t\ttarget.postKeyPressed(nextVertical < 0 ? Canvas.KEY_UP : Canvas.KEY_DOWN);
\t\t\t}
\t\t\tjoystickVertical = nextVertical;
\t\t}
\t}

\tprivate void releaseJoystick() {
\t\tif (target != null) {
\t\t\tif (joystickHorizontal != 0) {
\t\t\t\ttarget.postKeyReleased(joystickHorizontal < 0 ? Canvas.KEY_LEFT : Canvas.KEY_RIGHT);
\t\t\t}
\t\t\tif (joystickVertical != 0) {
\t\t\t\ttarget.postKeyReleased(joystickVertical < 0 ? Canvas.KEY_UP : Canvas.KEY_DOWN);
\t\t\t}
\t\t}
\t\tjoystickHorizontal = 0;
\t\tjoystickVertical = 0;
\t\tjoystickKnobX = joystickCenterX;
\t\tjoystickKnobY = joystickCenterY;
\t}

\tpublic void show() {
\t\tif (settings.vkHideDelay > 0 && obscuresVirtualScreen) {""")

replace_once(vk_path,
    """\t\t\tint alpha = (opaque || layoutEditMode != LAYOUT_EOF ? 0xFF : Math.max(settings.vkAlpha, 0xC0)) << 24;""",
    """\t\t\tint alpha = (layoutVariant == TYPE_SAINTS_ROW
\t\t\t\t\t? Math.max(settings.vkAlpha, 0x70)
\t\t\t\t\t: (opaque || layoutEditMode != LAYOUT_EOF ? 0xFF : Math.max(settings.vkAlpha, 0xC0))) << 24;""")

android_path = "javax/microedition/media/AndroidPlayer.java"
replace_once(android_path,
    """import android.media.MediaPlayer;

import java.io.IOException;

public class AndroidPlayer extends MediaPlayer {""",
    """import android.media.AudioAttributes;
import android.media.MediaPlayer;
import android.util.Log;

import java.io.IOException;

public class AndroidPlayer extends MediaPlayer {
\tprivate static final String TAG = "SaintsRowAudio";""")

replace_once(android_path,
    """\t@Override
\tpublic void setDataSource(String path) throws IOException, IllegalArgumentException, IllegalStateException, SecurityException {
\t\tthis.path = path;
\t}""",
    """\t@Override
\tpublic void setDataSource(String path) throws IOException, IllegalArgumentException, IllegalStateException, SecurityException {
\t\tif (loaded) {
\t\t\treset();
\t\t}
\t\tthis.path = path;
\t\tthis.timePos = 0;
\t}""")

replace_once(android_path,
    """\t@Override
\tpublic void start() throws IllegalStateException {
\t\tload();
\t\ttimePos = 0;
\t\tsuper.start();
\t}

\t@Override
\tpublic void reset() {
\t\tif (loaded) {
\t\t\tsuper.reset();
\t\t\tloaded = false;
\t\t}
\t}

\tprivate void load() {
\t\tif (!loaded) {
\t\t\ttry {
\t\t\t\tsuper.setDataSource(path);
\t\t\t\tsuper.prepare();
\t\t\t\tsuper.setVolume(leftVolume, rightVolume);
\t\t\t\tsuper.setLooping(looping);
\t\t\t\tsuper.seekTo(timePos);
\t\t\t} catch (IOException e) {
\t\t\t\te.printStackTrace();
\t\t\t}
\t\t\tloaded = true;
\t\t}
\t}""",
    """\t@Override
\tpublic void start() throws IllegalStateException {
\t\tload();
\t\tif (!loaded) {
\t\t\treturn;
\t\t}
\t\ttry {
\t\t\tsuper.start();
\t\t\ttimePos = 0;
\t\t} catch (IllegalStateException e) {
\t\t\tLog.e(TAG, "MediaPlayer could not start: " + path, e);
\t\t\ttry {
\t\t\t\tsuper.reset();
\t\t\t} catch (Throwable ignored) {
\t\t\t}
\t\t\tloaded = false;
\t\t}
\t}

\t@Override
\tpublic void pause() {
\t\tif (!loaded) {
\t\t\treturn;
\t\t}
\t\ttry {
\t\t\tsuper.pause();
\t\t} catch (IllegalStateException e) {
\t\t\tLog.w(TAG, "MediaPlayer pause ignored in its current state", e);
\t\t}
\t}

\t@Override
\tpublic void reset() {
\t\ttry {
\t\t\tsuper.reset();
\t\t} catch (IllegalStateException ignored) {
\t\t}
\t\tloaded = false;
\t\ttimePos = 0;
\t}

\tprivate void load() {
\t\tif (loaded) {
\t\t\treturn;
\t\t}
\t\tif (path == null || path.length() == 0) {
\t\t\tLog.e(TAG, "Audio source path is empty");
\t\t\treturn;
\t\t}
\t\ttry {
\t\t\tsuper.setAudioAttributes(new AudioAttributes.Builder()
\t\t\t\t\t.setUsage(AudioAttributes.USAGE_GAME)
\t\t\t\t\t.setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
\t\t\t\t\t.build());
\t\t\tsuper.setDataSource(path);
\t\t\tsuper.prepare();
\t\t\tsuper.setVolume(leftVolume, rightVolume);
\t\t\tsuper.setLooping(looping);
\t\t\tif (timePos > 0) {
\t\t\t\tsuper.seekTo(timePos);
\t\t\t}
\t\t\tloaded = true;
\t\t} catch (Exception e) {
\t\t\tLog.e(TAG, "Unable to prepare MIDlet audio source: " + path, e);
\t\t\ttry {
\t\t\t\tsuper.reset();
\t\t\t} catch (Throwable resetError) {
\t\t\t\tLog.w(TAG, "MediaPlayer reset after load failure failed", resetError);
\t\t\t}
\t\t\tloaded = false;
\t\t}
\t}""")

print("Applied Saints Row touch controls and audio reliability patches.")
