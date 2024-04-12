package game.example.android
import android.app.NativeActivity
import android.os.Bundle
import android.os.VibrationEffect
import android.os.Vibrator
import android.view.View

class MainActivity : NativeActivity() {
    public override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // https://developer.android.com/develop/ui/views/layout/immersive
        // https://developer.android.com/develop/ui/views/layout/edge-to-edge#system-gesture-insets
    }

    /**
     * "sticky immersive" full screen mode.
     * When user swipes from top/bottom edge, transparent status bar and navigation bar appear and slowly fade out if not used.
     * https://developer.android.com/training/system-ui/immersive
     */
    override fun onWindowFocusChanged(hasFocus: Boolean) {
        super.onWindowFocusChanged(hasFocus)
        if (hasFocus) hideSystemUi()
    }

    @Suppress("DEPRECATION")
    private fun hideSystemUi() {
        val decorView = window.decorView
        decorView.systemUiVisibility = (View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                or View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                or View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                or View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                or View.SYSTEM_UI_FLAG_FULLSCREEN)
    }

    public fun vibrate(milliseconds: Long, amplitude: Int) {
        val vibrator = getSystemService(Vibrator::class.java)
        if(!vibrator.hasVibrator()) return
        val effect = VibrationEffect.createOneShot(milliseconds, amplitude)
        vibrator.vibrate(effect)
    }

    public fun get_caches_directory(): String {
        return cacheDir.absolutePath
    }

    public fun get_documents_directory(): String {
        return filesDir.absolutePath
    }
}