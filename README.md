# Statistical-Process-Control-SPC
In high-precision manufacturing, such as CNC turning of automotive drive shafts, identifying dimensional anomalies before they result in scrap is critical. This project involves the development of a Python-based Automated Statistical Process Control (SPC) system designed to monitor real-time manufacturing variability and evaluate process capability ($C_{pk}$).

# Methodology & Implementation:
Data Simulation & Anomaly Injection: Engineered a synthetic dataset representing shaft diameter measurements ($50 \pm 0.05$ mm). Deliberately injected mathematical noise into the data array to simulate real-world physical manufacturing defects, specifically Tool Wear (mean drift) and Machine Spindle Vibration (variance expansion).
Algorithmic Monitoring: Developed a Python script utilizing NumPy and Matplotlib to autonomously compute subgroup statistics and generate dynamic $\bar{X}$ (X-bar) and $R$ control charts.
Capability Assessment: Integrated automated calculation of the Process Capability Index ($C_{pk}$), enabling quantitative evaluation of the machining process health against rigid Upper and Lower Specification Limits (USL/LSL).
# Engineering Value:
This system demonstrates the transition from traditional reactive quality control to predictive quality assurance. By visualizing out-of-control signals in the $\bar{X}-R$ charts, engineers can proactively halt production and recalibrate machinery, drastically minimizing the scrap rate and optimizing the Overall Equipment Effectiveness (OEE).
# Formula:
$$C_{pk} = \min \left( \frac{USL - \mu}{3\sigma}, \frac{\mu - LSL}{3\sigma} \right)$$
$$C_p = \frac{USL - LSL}{6\sigma}$$

<img width="908" height="452" alt="Screenshot 2026-06-05 050142" src="https://github.com/user-attachments/assets/cc94509c-b773-4428-8de9-c958c44169ba" />

