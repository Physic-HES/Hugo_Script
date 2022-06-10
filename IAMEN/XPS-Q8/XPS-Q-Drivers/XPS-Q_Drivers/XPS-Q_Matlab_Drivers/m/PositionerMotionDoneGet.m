function [errorCode, PositionWindow, VelocityWindow, CheckingTime, MeanPeriod, TimeOut] = PositionerMotionDoneGet(socketId, PositionerName)
%PositionerMotionDoneGet :  Read motion done parameters
%
%	[errorCode, PositionWindow, VelocityWindow, CheckingTime, MeanPeriod, TimeOut] = PositionerMotionDoneGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr PositionWindow
%		doublePtr VelocityWindow
%		doublePtr CheckingTime
%		doublePtr MeanPeriod
%		doublePtr TimeOut


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
PositionWindow = 0;
VelocityWindow = 0;
CheckingTime = 0;
MeanPeriod = 0;
TimeOut = 0;

% lib call
[errorCode, PositionerName, PositionWindow, VelocityWindow, CheckingTime, MeanPeriod, TimeOut] = calllib('XPS_Q8_drivers', 'PositionerMotionDoneGet', socketId, PositionerName, PositionWindow, VelocityWindow, CheckingTime, MeanPeriod, TimeOut);
