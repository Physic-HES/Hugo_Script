function [errorCode] = GroupInitializeWithEncoderCalibration(socketId, GroupName)
%GroupInitializeWithEncoderCalibration :  Group initialization with encoder calibration
%
%	[errorCode] = GroupInitializeWithEncoderCalibration(socketId, GroupName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName] = calllib('XPS_Q8_drivers', 'GroupInitializeWithEncoderCalibration', socketId, GroupName);
