"""SDG-SOAS: free, lightweight CLO classification interface."""
import csv
import io
import json
import streamlit as st
from engine import classify, load

st.set_page_config(page_title="SDG-SOAS | CLO Mapper", page_icon="🌍", layout="wide")
SDG_NAMES = {
 1:"No Poverty",2:"Zero Hunger",3:"Good Health and Well-being",4:"Quality Education",
 5:"Gender Equality",6:"Clean Water and Sanitation",7:"Affordable and Clean Energy",
 8:"Decent Work and Economic Growth",9:"Industry, Innovation and Infrastructure",
 10:"Reduced Inequalities",11:"Sustainable Cities and Communities",
 12:"Responsible Consumption and Production",13:"Climate Action",
 14:"Life Below Water",15:"Life on Land",16:"Peace, Justice and Strong Institutions",
 17:"Partnerships for the Goals"}

@st.cache_resource
def rules():
 return load()

st.title("🌍 SDG-SOAS: CLO-to-SDG Concept Mapper")
st.caption("Experimental concept-and-rule engine · Goal-level predictions · Free and open source")
st.info("Predictions are provisional and require academic review. They do not certify official UN target alignment.")
config=rules()
tab1,tab2=st.tabs(["Single CLO", "Batch CSV"])
with tab1:
 text=st.text_area("Enter a course learning outcome (CLO)",height=150,placeholder="Enter one CLO or several numbered CLOs…")
 if st.button("Classify CLO",type="primary",disabled=not text.strip()):
  output=classify(text,config)
  if output['sdgs']:
   st.subheader("Predicted SDGs")
   for number in output['sdgs']:
    st.markdown(f"**SDG {number} — {SDG_NAMES[number]}**")
    for evidence in output['matches'].get(str(number),[]):
     with st.expander(f"Evidence: {evidence['description']}"):
      st.write("Matched terms:")
      st.json(evidence['evidence'])
      st.write("CLO excerpt:",evidence['text'])
  else:
   st.warning("No SDG identified by the current rules. This is not proof of no SDG relevance.")
  st.caption("Review required: Yes")
with tab2:
 st.write("Upload a CSV containing a CLO text column. The file is processed in application memory; this application does not save it to disk.")
 uploaded=st.file_uploader("Choose CSV",type=["csv"])
 if uploaded is not None:
  try:
   raw=uploaded.getvalue().decode('utf-8-sig')
   rows=list(csv.DictReader(io.StringIO(raw)))
   if not rows:
    st.warning("CSV has no data rows.")
   else:
    col=st.selectbox("CLO text column",list(rows[0].keys()))
    idcol=st.selectbox("Optional course/record ID column",["(row number)"]+list(rows[0].keys()))
    if st.button("Classify CSV",type="primary"):
     output=[]
     for i,row in enumerate(rows,1):
      result=classify(row.get(col,'') or '',config)
      output.append({"record_id":i if idcol=="(row number)" else row.get(idcol,''),
       "clo_text":row.get(col,''),"predicted_sdgs":";".join(map(str,result['sdgs'])),
       "review_required":"Yes", "evidence_json":json.dumps(result['matches'],ensure_ascii=False)})
     st.write(f"Processed {len(output)} rows")
     st.dataframe(output,use_container_width=True)
     buffer=io.StringIO()
     writer=csv.DictWriter(buffer,fieldnames=list(output[0].keys()))
     writer.writeheader();writer.writerows(output)
     st.download_button("Download predictions CSV",buffer.getvalue().encode('utf-8-sig'),file_name="sdg_predictions.csv",mime="text/csv")
  except (UnicodeDecodeError,csv.Error) as exc:
   st.error(f"Could not read CSV: {exc}")
with st.expander("About this prototype and privacy"):
 st.write("The rules use transparent concept combinations and may miss implicit relationships or unfamiliar wording. No model training or paid AI service is used.")
 st.write("On Streamlit Community Cloud, submitted text is processed by the hosted server, not by your Mac. Avoid entering confidential or personal information into a public app.")
 st.write("No authentication is configured; anyone with the deployed URL may use the application. Hosting limits and platform data practices apply.")
