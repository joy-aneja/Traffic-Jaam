package com.example.pagefragmenrtactivity;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.List;
import java.util.Locale;

import org.achartengine.ChartFactory;
import org.achartengine.GraphicalView;
import org.achartengine.chart.PointStyle;
import org.achartengine.model.SeriesSelection;
import org.achartengine.model.TimeSeries;
import org.achartengine.model.XYMultipleSeriesDataset;
import org.achartengine.model.XYSeries;
import org.achartengine.renderer.XYMultipleSeriesRenderer;
import org.achartengine.renderer.XYSeriesRenderer;

import android.graphics.Color;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.app.Activity;
import android.app.ActionBar;
import android.app.AlarmManager;
import android.app.AlertDialog;
import android.app.DatePickerDialog;
import android.app.Dialog;
import android.app.Fragment;
import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.app.PendingIntent;
import android.app.TimePickerDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.support.v13.app.FragmentPagerAdapter;
import android.media.RingtoneManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.net.http.AndroidHttpClient;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.DialogFragment;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.NotificationCompat;
import android.support.v4.view.ViewPager;
import android.text.InputFilter;
import android.text.format.DateFormat;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.TimePicker;
import android.widget.Toast;

public class MainActivity extends FragmentActivity implements
		ActionBar.TabListener
{
	SectionsPagerAdapter mSectionsPagerAdapter;
	ViewPager mViewPager;
	private String[] days = new String[] { "Mon", "Tue", "Wed", "Thurs", "Fri",
			"Sat", "Sun", "Mon" };
	
	public String home="", work="";

	public static long INTERVAL_FIFTEEN_MINUTES = 60 * 1000L;
	// public static TextView homeLocationTextview, alarmTextView;
	public static NotificationCompat.Builder mBuilder;
	public static int alarmHour, alarmMinute;
	public static Boolean alarmSet = false;
	public PendingIntent trafficAlarmPendingIntent;
	public AlarmManager trafficAlarmManager;
	public String strName;
	public GraphicalView graph;

	@Override
	protected void onCreate(Bundle savedInstanceState)
	{
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		mBuilder = new NotificationCompat.Builder(this)
				.setSmallIcon(R.drawable.alarm_clock_icon)
				.setContentTitle("Traffic Jaam")
				.setSound(
						RingtoneManager
								.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION));

		// Set up the action bar.
		final ActionBar actionBar = getActionBar();
		actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_TABS);

		// Create the adapter that will return a fragment for each of the three
		// primary sections of the activity.
		mSectionsPagerAdapter = new SectionsPagerAdapter(getFragmentManager());

		// Set up the ViewPager with the sections adapter.
		mViewPager = (ViewPager) findViewById(R.id.pager);
		mViewPager.setAdapter(mSectionsPagerAdapter);

		// When swiping between different sections, select the corresponding
		// tab. We can also use ActionBar.Tab#select() to do this if we have
		// a reference to the Tab.
		mViewPager
				.setOnPageChangeListener(new ViewPager.SimpleOnPageChangeListener()
				{
					@Override
					public void onPageSelected(int position)
					{
						actionBar.setSelectedNavigationItem(position);
					}
				});

		// For each of the sections in the app, add a tab to the action bar.
		for (int i = 0; i < mSectionsPagerAdapter.getCount(); i++)
		{
			// Create a tab with text corresponding to the page title defined by
			// the adapter. Also specify this Activity object, which implements
			// the TabListener interface, as the callback (listener) for when
			// this tab is selected.
			actionBar.addTab(actionBar.newTab()
					.setText(mSectionsPagerAdapter.getPageTitle(i))
					.setTabListener(this));
		}
	}

	public void onLeadTimeClick(View v)
	{
		LeadTimeDialogFragment leadTimeDialogFragment = new LeadTimeDialogFragment();
		leadTimeDialogFragment.show(getSupportFragmentManager(),
				"leadTimeDialog");
	}
	
	public void onWorkLocationClick(View v)
	{
		WorkLocationDialogFragment workLocationDialogFragment = new WorkLocationDialogFragment();
		workLocationDialogFragment.show(getSupportFragmentManager(),"workDialog");
	}
	
	public void onHomeLocationClick(View v)
	{
		HomeLocationDialogFragment homeLocationDialogFragment = new HomeLocationDialogFragment();
		homeLocationDialogFragment.show(getSupportFragmentManager(),"homeDialog");
	}
	
	

	public void onSetAlarmButtonClick(View v)
	{
		DialogFragment newFragment = new TimePickerFragment();
		newFragment.show(getSupportFragmentManager(), "timePicker");
	}

	public void onSetGraphTimeClick(View v)
	{
		AlertDialog.Builder builderSingle = new AlertDialog.Builder(this);
		builderSingle.setIcon(R.drawable.ic_launcher);
		builderSingle.setTitle("Select Time:-");
		final ArrayAdapter<String> arrayAdapter = new ArrayAdapter<String>(
				this, android.R.layout.select_dialog_singlechoice);
		arrayAdapter.add("8");
		arrayAdapter.add("9");
		arrayAdapter.add("10");
		arrayAdapter.add("11");
		arrayAdapter.add("12");
		arrayAdapter.add("13");
		arrayAdapter.add("14");
		arrayAdapter.add("15");
		arrayAdapter.add("16");
		arrayAdapter.add("17");
		arrayAdapter.add("18");
		arrayAdapter.add("19");
		arrayAdapter.add("20");
		arrayAdapter.add("21");
		arrayAdapter.add("22");
		arrayAdapter.add("23");
		builderSingle.setNegativeButton("cancel",
				new DialogInterface.OnClickListener()
				{

					@Override
					public void onClick(DialogInterface dialog, int which)
					{
						dialog.dismiss();
					}
				});

		builderSingle.setAdapter(arrayAdapter,
				new DialogInterface.OnClickListener()
				{

					@Override
					public void onClick(DialogInterface dialog, int which)
					{
						strName = arrayAdapter.getItem(which);

						new HttpAsyncTask()
								.execute("http://py-scheduler.appspot.com/getdigest?hour="
										+ Integer.parseInt(strName)
										+ "&source=28.549291,77.267814&dest=28.556162,77.099958");
						TextView graphTextView = (TextView) findViewById(R.id.graphTextView);
						int graphTime = Integer.parseInt(strName);
						if (graphTime > 12)
							graphTextView.setText((graphTime - 12) + " pm");
						else if (graphTime == 12)
							graphTextView.setText(strName + " pm");
						else
							graphTextView.setText(strName + " am");
					}
				});
		builderSingle.show();
	}

	public void onCancelAlarmButtonClick(View v)
	{
		if (trafficAlarmManager != null)
		{
			final TextView alarmTextView = (TextView) findViewById(R.id.alarmTextView);
			trafficAlarmManager.cancel(trafficAlarmPendingIntent);
			alarmTextView.setText(R.string.setAlarm);
			Toast.makeText(getApplicationContext(), "Alarm cancelled",
					Toast.LENGTH_LONG).show();
		}
	}

	public class DatePickerFragment extends DialogFragment implements
			DatePickerDialog.OnDateSetListener
	{
		@Override
		public Dialog onCreateDialog(Bundle savedInstanceState)
		{
			// Use the current date as the default date in the picker
			final Calendar c = Calendar.getInstance();
			int year = c.get(Calendar.YEAR);
			int month = c.get(Calendar.MONTH);
			int day = c.get(Calendar.DAY_OF_MONTH);

			// Create a new instance of DatePickerDialog and return it after
			// setting max date
			DatePickerDialog dpDialog = new DatePickerDialog(getActivity(),
					this, year, month, day);
			dpDialog.getDatePicker().setMaxDate(new Date().getTime());
			return dpDialog;
		}

		// Method to detect when Date is selected by user from DatePicker and
		// then return the selected value
		public void onDateSet(DatePicker view, int year, int month, int day)
		{
		}
	}

	public class TimePickerFragment extends DialogFragment implements
			TimePickerDialog.OnTimeSetListener
	{
		@Override
		public Dialog onCreateDialog(Bundle savedInstanceState)
		{
			// Use the current time as the default values for the picker
			final Calendar c = Calendar.getInstance();
			int hour = c.get(Calendar.HOUR_OF_DAY);
			int minute = c.get(Calendar.MINUTE);
			alarmSet = false;

			// Create a new instance of TimePickerDialog and return it
			final TimePickerDialog tpDialog = new TimePickerDialog(
					getActivity(), this, hour, minute,
					DateFormat.is24HourFormat(getActivity()));
			tpDialog.setCancelable(true);
			tpDialog.setButton(DialogInterface.BUTTON_NEGATIVE, "Cancel",
					new DialogInterface.OnClickListener()
					{
						@Override
						public void onClick(DialogInterface dialog, int which)
						{
							alarmSet = false;
							tpDialog.dismiss();
						}
					});
			tpDialog.setButton(DialogInterface.BUTTON_POSITIVE, "Set",
					new DialogInterface.OnClickListener()
					{
						@Override
						public void onClick(DialogInterface dialog, int which)
						{
							alarmSet = true;
						}
					});
			return tpDialog;
		}

		public void onTimeSet(TimePicker view, int hourOfDay, int minute)
		{
			final TextView alarmTextView = (TextView) findViewById(R.id.alarmTextView);
			alarmHour = hourOfDay;
			alarmMinute = minute;
			if (alarmSet)
			{
				trafficAlarmManager = (AlarmManager) getSystemService(ALARM_SERVICE);
				Intent trafficAlarmIntent = new Intent(getActivity(),
						TrafficJaamAlertService.class);
				trafficAlarmPendingIntent = PendingIntent.getService(
						getActivity(), 0, trafficAlarmIntent, 0);

				Calendar calendar = Calendar.getInstance();
				calendar.setTimeInMillis(System.currentTimeMillis());
				calendar.set(Calendar.HOUR_OF_DAY, alarmHour - 2);
				calendar.set(Calendar.MINUTE, alarmMinute);
				trafficAlarmManager.setRepeating(AlarmManager.RTC_WAKEUP,
						calendar.getTimeInMillis(), INTERVAL_FIFTEEN_MINUTES,
						trafficAlarmPendingIntent);
				alarmTextView.setText(alarmHour + " : " + alarmMinute);
				Toast.makeText(getActivity(),
						"Alarm set for " + alarmHour + " : " + alarmMinute,
						Toast.LENGTH_SHORT).show();
			}
		}
	}

	public class LeadTimeDialogFragment extends DialogFragment
	{
		public Dialog onCreateDialog(Bundle savedInstanceState)
		{
			final TextView leadTimeTextView = (TextView) findViewById(R.id.leadTimeTextview);
			AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
			builder.setTitle("Lead Time");
			builder.setMessage("Set Lead Time (mins):");
			final EditText leadTimeEditText = new EditText(MainActivity.this);
			// LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
			// 1,
			// 2);
			// leadTimeEditText.setLayoutParams(lp);
			leadTimeEditText.setWidth(10);
			leadTimeEditText
					.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
			int maxLength = 2;
			InputFilter[] fArray = new InputFilter[1];
			fArray[0] = new InputFilter.LengthFilter(maxLength);
			leadTimeEditText.setFilters(fArray);
			builder.setView(leadTimeEditText);
			builder.setPositiveButton("OK",
					new DialogInterface.OnClickListener()
					{
						public void onClick(DialogInterface dialog,
								int whichButton)
						{
							if (!leadTimeEditText.getText().toString()
									.isEmpty())
							{
								int leadTime = Integer
										.parseInt(leadTimeEditText.getText()
												.toString());
								leadTimeTextView.setText(Integer
										.toString(leadTime) + " mins");
							} else
								leadTimeTextView
										.setText(R.string.set_lead_time);
							dismiss();
						}
					});
			return builder.create();
		}
	}
	
	public class HomeLocationDialogFragment extends DialogFragment
	{
		public Dialog onCreateDialog(Bundle savedInstanceState)
		{
			final TextView homeLocationTextView = (TextView) findViewById(R.id.homeLocationTextview);
			AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
			builder.setTitle("Home Location");
			builder.setMessage("Set Home Location");
			final EditText homeLocationEditText = new EditText(MainActivity.this);
			// LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
			// 1,
			// 2);
			// leadTimeEditText.setLayoutParams(lp);
			homeLocationEditText.setWidth(22);
			//homeLocationEditText
			//		.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
			//int maxLength = 2;
			//InputFilter[] fArray = new InputFilter[1];
			//fArray[0] = new InputFilter.LengthFilter(maxLength);
			//leadTimeEditText.setFilters(fArray);
			builder.setView(homeLocationEditText);
			builder.setPositiveButton("OK",
					new DialogInterface.OnClickListener()
					{
						public void onClick(DialogInterface dialog,
								int whichButton)
						{
							if (!homeLocationEditText.getText().toString()
									.isEmpty())
							{
								String location = homeLocationEditText.getText().toString();
												
								homeLocationTextView.setText(location);
							} else
								homeLocationTextView
										.setText(R.string.home_location);
							dismiss();
						}
					});
			return builder.create();
		}
	}
	
	
	public class WorkLocationDialogFragment extends DialogFragment
	{
		public Dialog onCreateDialog(Bundle savedInstanceState)
		{
			final TextView workLocationTextView = (TextView) findViewById(R.id.workLocationTextview);
			AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
			builder.setTitle("Work Location");
			builder.setMessage("Set Work Location");
			final EditText workLocationEditText = new EditText(MainActivity.this);
			// LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
			// 1,
			// 2);
			// leadTimeEditText.setLayoutParams(lp);
			workLocationEditText.setWidth(22);
			//workLocationEditText
				//	.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
			//int maxLength = 2;
			//InputFilter[] fArray = new InputFilter[1];
			//fArray[0] = new InputFilter.LengthFilter(maxLength);
			//leadTimeEditText.setFilters(fArray);
			builder.setView(workLocationEditText);
			builder.setPositiveButton("OK",
					new DialogInterface.OnClickListener()
					{
						public void onClick(DialogInterface dialog,
								int whichButton)
						{
							if (!workLocationEditText.getText().toString()
									.isEmpty())
							{
								String location = workLocationEditText.getText().toString();
								work = location;
												
								workLocationTextView.setText(location);
							} else
								workLocationTextView
										.setText(R.string.work_location);
							dismiss();
						}
					});
			return builder.create();
		}
	}


	@Override
	public boolean onCreateOptionsMenu(Menu menu)
	{
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item)
	{
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings)
		{
			return true;
		}
		return super.onOptionsItemSelected(item);
	}

	@Override
	public void onTabSelected(ActionBar.Tab tab,
			FragmentTransaction fragmentTransaction)
	{
		// When the given tab is selected, switch to the corresponding page in
		// the ViewPager.
		mViewPager.setCurrentItem(tab.getPosition());
	}

	@Override
	public void onTabUnselected(ActionBar.Tab tab,
			FragmentTransaction fragmentTransaction)
	{
	}

	@Override
	public void onTabReselected(ActionBar.Tab tab,
			FragmentTransaction fragmentTransaction)
	{
	}

	/**
	 * A {@link FragmentPagerAdapter} that returns a fragment corresponding to
	 * one of the sections/tabs/pages.
	 */
	public class SectionsPagerAdapter extends FragmentPagerAdapter
	{

		public SectionsPagerAdapter(FragmentManager fm)
		{
			super(fm);
		}

		@Override
		public Fragment getItem(int position)
		{
			// getItem is called to instantiate the fragment for the given page.
			// Return a PlaceholderFragment (defined as a static inner class
			// below).
			if (position == 0)
				return new Home();
			else
				return new graph();
		}

		@Override
		public int getCount()
		{
			// Show 2 total pages.
			return 2;
		}

		@Override
		public CharSequence getPageTitle(int position)
		{
			Locale l = Locale.getDefault();
			switch (position)
			{
			case 0:
				return getString(R.string.title_section1).toUpperCase(l);
			case 1:
				return getString(R.string.title_section2).toUpperCase(l);
			}
			return null;
		}
	}

	/**
	 * A placeholder fragment containing a simple view.
	 */
	public static class PlaceholderFragment extends Fragment
	{
		/**
		 * The fragment argument representing the section number for this
		 * fragment.
		 */
		private static final String ARG_SECTION_NUMBER = "section_number";

		/**
		 * Returns a new instance of this fragment for the given section number.
		 */
		public static PlaceholderFragment newInstance(int sectionNumber)
		{
			PlaceholderFragment fragment = new PlaceholderFragment();
			Bundle args = new Bundle();
			args.putInt(ARG_SECTION_NUMBER, sectionNumber);
			fragment.setArguments(args);
			return fragment;
		}

		public PlaceholderFragment()
		{
		}

		@Override
		public View onCreateView(LayoutInflater inflater, ViewGroup container,
				Bundle savedInstanceState)
		{
			View rootView = inflater.inflate(R.layout.fragment_main, container,
					false);
			return rootView;
		}
	}

	// Graph Plot - Dangerous. Trespassing not allowed

	public static String GET(String url)
	{
		InputStream inputStream = null;
		String result = "";
		try
		{

			HttpClient httpclient = new DefaultHttpClient();
			HttpResponse httpResponse = httpclient.execute(new HttpGet(url));
			inputStream = httpResponse.getEntity().getContent();
			if (inputStream != null)
				result = convertInputStreamToString(inputStream);
			else
				result = "Connection failure!";

		} catch (Exception e)
		{
			Log.d("InputStream", e.getLocalizedMessage());
		}

		return result;
	}

	private static String convertInputStreamToString(InputStream inputStream)
			throws IOException
	{
		BufferedReader bufferedReader = new BufferedReader(
				new InputStreamReader(inputStream));
		String line = "";
		String result = "";
		while ((line = bufferedReader.readLine()) != null)
			result += line;

		inputStream.close();
		return result;

	}

	public boolean isConnected()
	{
		ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Activity.CONNECTIVITY_SERVICE);
		NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
		if (networkInfo != null && networkInfo.isConnected())
			return true;
		else
			return false;
	}

	private class HttpAsyncTask extends AsyncTask<String, Void, String>
	{

		AndroidHttpClient client = AndroidHttpClient.newInstance("");

		@Override
		protected String doInBackground(String... urls)
		{

			return GET(urls[0]);
		}

		// onPostExecute displays the results of the AsyncTask.
		@Override
		protected void onPostExecute(String result)
		{

			if (null != client)
				client.close();
			try
			{
				JSONObject json = new JSONObject(result);
				JSONArray week1 = json.getJSONObject("data").getJSONObject("week1").getJSONArray("toj");
				String estimated_toj = json.getJSONObject("data").getString("estimatedtoj");
				String week_id = json.getJSONObject("data").getString("week");
				String c_day = json.getString("cday");
				int curr_day=Integer.parseInt(c_day);
				double estimated_time = Double.parseDouble(estimated_toj);
				
				String[] week1_day = new String[7];
				String[] week1_date = new String[7];
				Double[] week1_time = new Double[7];
				
				for(int i = 0;i<7;i++)
				{
					 JSONObject day_no = week1.getJSONObject(i);
					 String time = day_no.getString("toj");
					 week1_date[i] = day_no.getString("date");
					 week1_day[i] =day_no.getString("day");
					 if(time.equals("None"))
					 {
						 time="0";
					 }
					 
					 week1_time[i]=Double.parseDouble(time);
					
				}
				
				JSONArray week2 = json.getJSONObject("data").getJSONObject("week2").getJSONArray("toj");
				Double[] week2_time = new Double[7];
				String[] week2_day = new String[7];
				String[] week2_date = new String[7];
				for(int i = 0;i<7;i++)
				{
					 JSONObject day_no = week2.getJSONObject(i);
					 String time = day_no.getString("toj");
					 week2_date[i] = day_no.getString("date");
					 week2_day[i] =day_no.getString("day");
					 if(time.equals("None"))
					 {
						 time="0";
					 }
					 week2_time[i]=Double.parseDouble(time);
				} 
				//int curr_day=0;
				int k=curr_day,j=0;
				int array_length=week1_time.length + week2_time.length;
				Double[] combined_time = new Double[array_length];
				Double[] current_time = new Double[week1_time.length+1];
				Double[] previous_time = new Double[week2_time.length+1];
				if(week_id=="1"){
					for(int i = 0;i<array_length;i++)
					{
						System.arraycopy(week1_time, 0, combined_time, 0, week1_time.length);
						System.arraycopy(week2_time, 0, combined_time, week1_time.length, week2_time.length);
					}
					
					for(int i=1; i<= week1_time.length;i++)
					{
						previous_time[i-1]=combined_time[(k+i)%14]; 
						j=(k+i+1)%14;
					}
					
					for(int i=0; i< week1_time.length;i++)
					{
						current_time[i]=combined_time[(j+i)%14]; 
					}
					
				}
				else
				{

					System.arraycopy(week2_time, 0, combined_time, 0, week2_time.length);
					System.arraycopy(week1_time, 0, combined_time, week2_time.length, week1_time.length);
					
					for(int i=1; i<= week1_time.length+1;i++)
					{
						previous_time[i-1]=combined_time[(k+i)%14]; 
						j=(k+i+1)%14;
					}
					
					for(int i=0; i< week1_time.length+1;i++)
					{
						current_time[i]=combined_time[(j+i)%14]; 
					}
					
				}
				Double[] es_time = new Double[current_time.length+1];
				for(int i=0; i< current_time.length+1;i++)
				{
					es_time[i]=0.0;
					
				}
				es_time[6]=combined_time[curr_day];
				es_time[7]=(Double)estimated_time;						        
		        
		         int[] days_xaxis= new int[8]; 
		         int x=curr_day;
				 for(int i=0; i<=7;i++)
				 {
					   days_xaxis[i]=(x+1)%7;
					   x++;
					    
				 }
		        
				    TimeSeries week1_series = new TimeSeries("Current Week");
				    TimeSeries week2_series = new TimeSeries("Previous Week");
		        	
				    TimeSeries estimated_toj_series = new TimeSeries("Estimated TOJ");
		        	
		        	for(int i=0;i<days_xaxis.length;i++){
		        		if(current_time[i]!=0.0)
		        		{
		        		week1_series.add(days_xaxis[i], current_time[i]);
		        		
		        		}
		        		if(previous_time[i]!=0.0)
		        		{
		        		week2_series.add(days_xaxis[i],previous_time[i]);
		        		}
		        		
		        	}
		        	for(int i=0;i<days_xaxis.length;i++){
		        		if(es_time[i]!=0.0)
		        		{
		        			estimated_toj_series.add(i,es_time[i]);
		        		}
		        	}
		        	        	
		        	
		        	XYMultipleSeriesDataset graph_dataset = new XYMultipleSeriesDataset();
		        	graph_dataset.addSeries(week1_series);
		        	graph_dataset.addSeries(week2_series);    	
		        	graph_dataset.addSeries(estimated_toj_series);
		        	
		        	XYSeriesRenderer week1_renderer = new XYSeriesRenderer();
		        	week1_renderer.setColor(Color.GREEN);
		        	week1_renderer.setPointStyle(PointStyle.CIRCLE);
		        	week1_renderer.setFillPoints(true);
		        	week1_renderer.setLineWidth(2);
		        	week1_renderer.setDisplayChartValues(true);
		        	week1_renderer.isDisplayChartValues();
		        	week1_renderer.setFillBelowLine(true);
		        	
		        	XYSeriesRenderer week2_renderer = new XYSeriesRenderer();
		        	week2_renderer.setColor(Color.BLUE);
		        	week2_renderer.setPointStyle(PointStyle.CIRCLE);
		        	week2_renderer.setFillPoints(true);
		        	week2_renderer.setLineWidth(2);
		        	week2_renderer.setDisplayChartValues(true);
		        	week2_renderer.isDisplayChartValues();
		        	week2_renderer.setFillBelowLine(true);
		        	
		        	XYSeriesRenderer estimated_toj_renderer = new XYSeriesRenderer();
		        	estimated_toj_renderer.setColor(Color.RED);
		        	estimated_toj_renderer.setPointStyle(PointStyle.CIRCLE);
		        	estimated_toj_renderer.setFillPoints(true);
		        	estimated_toj_renderer.setLineWidth(2);
		        	estimated_toj_renderer.setDisplayChartValues(true);
		        	estimated_toj_renderer.isDisplayChartValues();
		        	estimated_toj_renderer.setFillBelowLine(true);
		        	
		        	
		        	
		        	XYMultipleSeriesRenderer multi_renderer = new XYMultipleSeriesRenderer();
		        	multi_renderer.setXLabels(0);
		        	multi_renderer.setChartTitle("Time of journey Chart");
		        	multi_renderer.setXTitle(" Week");
		        	multi_renderer.setYTitle("Time in Seconds");
		        	multi_renderer.setZoomButtonsVisible(true); 
		        	
		        	for(int i=0;i<days_xaxis.length;i++){
		        		multi_renderer.addXTextLabel(i, days[days_xaxis[i]]);  
		        		
		        	}    	
		        	
		        	
		        	multi_renderer.addSeriesRenderer(week1_renderer);
		        	multi_renderer.addSeriesRenderer(week2_renderer);
		        	multi_renderer.addSeriesRenderer(estimated_toj_renderer);

				multi_renderer.setClickEnabled(true);
				multi_renderer.setSelectableBuffer(10);

				LinearLayout chart_container = (LinearLayout) findViewById(R.id.linearLayout2);
				if (graph != null)
				{
					chart_container.removeView(graph);
				}
				graph = (GraphicalView) ChartFactory.getLineChartView(
						getBaseContext(), graph_dataset, multi_renderer);
				graph.setOnClickListener(new View.OnClickListener()
				{
					@Override
					public void onClick(View v)
					{

						SeriesSelection series_selection = graph
								.getCurrentSeriesAndPoint();

						if (series_selection != null)
						{
							int series_index = series_selection
									.getSeriesIndex();
							String selected_series = "Week1";
							if (series_index == 0)
								selected_series = "Week1";
							else if (series_index == 1)
								selected_series = "Week2";
							else
								selected_series = "Estimated TOJ";

							String day = days[(int) series_selection
									.getXValue()];

							int time = (int) series_selection.getValue();
							Toast.makeText(
									getBaseContext(),
									selected_series + " TOJ on " + day + " is "
											+ time + "secs", Toast.LENGTH_SHORT)
									.show();
						}
					}

				});

				chart_container.addView(graph);

			} catch (JSONException e)
			{
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}

}
