function [errorCode] = TZPVTExecution(socketId, GroupName, TrajectoryFileName, ExecutionNumber)
%TZPVTExecution :  TZ PVT trajectory execution
%
%	[errorCode] = TZPVTExecution(socketId, GroupName, TrajectoryFileName, ExecutionNumber)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		cstring TrajectoryFileName
%		int32 ExecutionNumber
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName, TrajectoryFileName] = calllib('XPS_C8_drivers', 'TZPVTExecution', socketId, GroupName, TrajectoryFileName, ExecutionNumber);
