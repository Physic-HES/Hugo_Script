function [errorCode] = PositionerMotionDoneSet(socketId, PositionerName, PositionWindow, VelocityWindow, CheckingTime, MeanPeriod, TimeOut)
%PositionerMotionDoneSet :  Update motion done parameters
%
%	[errorCode] = PositionerMotionDoneSet(socketId, PositionerName, PositionWindow, VelocityWindow, CheckingTime, MeanPeriod, TimeOut)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double PositionWindow
%		double VelocityWindow
%		double CheckingTime
%		double MeanPeriod
%		double TimeOut
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerMotionDoneSet', socketId, PositionerName, PositionWindow, VelocityWindow, CheckingTime, MeanPeriod, TimeOut);
