function [errorCode, SettingTime, SettlingTime] = PositionerSGammaPreviousMotionTimesGet(socketId, PositionerName)
%PositionerSGammaPreviousMotionTimesGet :  Read SettingTime and SettlingTime
%
%	[errorCode, SettingTime, SettlingTime] = PositionerSGammaPreviousMotionTimesGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr SettingTime
%		doublePtr SettlingTime


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
SettingTime = 0;
SettlingTime = 0;

% lib call
[errorCode, PositionerName, SettingTime, SettlingTime] = calllib('XPS_Q8_drivers', 'PositionerSGammaPreviousMotionTimesGet', socketId, PositionerName, SettingTime, SettlingTime);
