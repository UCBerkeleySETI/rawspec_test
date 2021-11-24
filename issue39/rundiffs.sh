source rungpu.cfg

echo 
echo diff for ics
diff gpu$GPUA.ics.tbldsel gpu$GPUB.ics.tbldsel
echo 
echo diff for ant001
diff gpu$GPUA.ant001.tbldsel gpu$GPUB.ant001.tbldsel
echo 
echo diff for ant000
diff gpu$GPUA.ant000.tbldsel gpu$GPUB.ant000.tbldsel
