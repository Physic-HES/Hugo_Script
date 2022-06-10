function [errorCode] = MultipleAxesPVTVerification(socketId, GroupName, TrajectoryFileName)
%MultipleAxesPVTVerification :  Multiple axes PVT trajectory verification
%
%	[errorCode] = MultipleAxesPVTVerification(socketId, GroupName, TrajectoryFileName)
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
[errorCode, GroupName, TrajectoryFileName] = calllib('XPS_Q8_drivers', 'MultipleAxesPVTVerification', socketId, GroupName, TrajectoryFileName);
