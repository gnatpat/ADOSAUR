Information
on SAD-Learning study face data

July
15, 2015

created
by Leonie Koban (leonie.koban@colorado.edu)

**General
study information**:

This
study investigates how socially anxious (SAD) versus healthy control
participants (HC) experience a stressful social speech task and how
they respond to and learn from social feedback regarding this speech
task.

We
are currently writing a manuscript describing the behavioral results
(Koban, et al. in prep.).

Facial
expressions were recorded using a webcam while participants were
sitting in front of a computer screen and performing the feedback
task. Facet was used to automatically encode intensity and evidence
of facial expressions (contact Yoni Ashar for more information,
yoniashar@gmail.com).

Given
that triggering was not working correctly, trial timings were
reconstructed using eprime output and timing of first response in
video data.

These
timings were then used to segment the facial expression data into
epochs (for each trial). Each epoch starts at the time of feedback
presentation (?verify with Yoni).

**Files
in FaceData_Sharing folder**:

**FeedbackTaskDesign.pptx**	illustrates
the design of the feedback task

**SADparticipant_group_LKcorrected.csv**
	contains information about group status of each participant (P =
patient/SAD, C = healthy control)

**1XX_facet_output.txt**
	files contain output (processed) time-series data from individual
participants (headers should be self-explaining) across the whole
duration of the feedback task

**trial_frames_evidence.mat**
	contains epoched (trial-wise) evidence time-series data for each
participant

**trial_frames_intensity.mat
	**contains
epoched (trial-wise) intensity  time-series data for each participant

**behavioral.mat**
	contains other (behavioral) data from the feedback task that is
hypothetically influencing emotional state and expressions of the 55
participants (one additional participant, #102, does not have facial
expression data):

	fbdata.selfevalr
is the participants own evaluation on each trial (each cell contains
data from each participant’s ratings in 58 trials)

	fbdata.selfevalrt
are the reaction times (RTs) for these self-evaluations 

	fbdata.selfevalr_t2
is the second evaluation for this specific item (in a second round of
the task 20min later)

	fbdata.selfeval_adj
is the difference between fbdata.selfevalr_t2 and fbdata.selfevalr
(how much participants change their self-evaluation from time 1 to
time 2)

	fbdata.judgeevalr
is the feedback from the judges

	fbdata.selffeel
is the trial wise rating of how participants feel about themselves

	fbdata.selffeelrt
is the corresponding RTs

	fbdata.judgefeel
is the trial wise rating of how participants feel about the judges

	fbdata.judgefeelrt
is the corresponding RTs

	fbdata.fbpe
is the difference between judges feedback and self-evaluation
(fbdata.judgeevalr - fbdata.selfevalr)

	fbdata.selffeelchange
is the trial wise change in feeling about the self

	fbdata.judgefeelchange
is the trial wise change in feeling about the judges

**Potential
questions to ask**:

Can
facial expression data overall separate patients from controls?

Can
facial expression responses to feedback separate patients from
controls?

Can
facial expressions predict what kind of feedback people got from
judges (fbdata.judgeevalr)?

Can
facial expressions predict how they rate their feelings towards the
self (fbdata.selffeel) / towards the judges (fbdata.judgefeel)?

Can
facial expressions predict how they change their performance ratings
(fbdata.selfeval_adj)?

etc.
