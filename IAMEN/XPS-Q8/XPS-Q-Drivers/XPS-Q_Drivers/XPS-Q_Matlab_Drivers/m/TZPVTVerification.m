function [errorCode] = TZPVTVerification(socketId, GroupName, TrajectoryFileName)
%TZPVTVerification :  TZ PVT trajectory verification
%
%	[errorCode] = TZPVTVerification(socketId, GroupName, TrajectoryFileName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		cstring TrajectoryFileName
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName, TrajectoryFileName] = calllib('XPS_C8_drivers', 'TZPVTVerification', socketId, GroupName, TrajectoryFileName);
