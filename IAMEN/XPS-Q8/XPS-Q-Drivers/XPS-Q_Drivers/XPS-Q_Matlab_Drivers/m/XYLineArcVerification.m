function [errorCode] = XYLineArcVerification(socketId, GroupName, TrajectoryFileName)
%XYLineArcVerification :  XY trajectory verification
%
%	[errorCode] = XYLineArcVerification(socketId, GroupName, TrajectoryFileName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		cstring TrajectoryFileName
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName, TrajectoryFileName] = calllib('XPS_Q8_drivers', 'XYLineArcVerification', socketId, GroupName, TrajectoryFileName);
