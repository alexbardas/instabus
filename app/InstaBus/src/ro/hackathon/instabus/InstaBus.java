package ro.hackathon.instabus;

import android.os.Bundle;

import org.apache.cordova.DroidGap;

/**
 * Main activity.
 * 
 * Load the index file for the InstaBus web-app.
 *
 * @author Alexandru Marinescu (almarinescu@gmail.com)
 */
public class InstaBus extends DroidGap {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        loadUrl("file:///android_asset/www/index.html");
    }
}
