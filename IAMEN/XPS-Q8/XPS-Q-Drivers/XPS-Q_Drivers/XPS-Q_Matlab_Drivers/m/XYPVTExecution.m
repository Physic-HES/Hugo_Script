function [errorCode] = XYPVTExecution(socketId, GroupName, TrajectoryFileName, ExecutionNumber)
%XYPVTExecution :  XY PVT trajectory execution
%
%	[errorCode] = XYPVTExecution(socketId, GroupName, TrajectoryFileName, ExecutionNumber)
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
[errorCode, GroupName, TrajectoryFileName] = calllib('XPS_C8_drivers', 'XYPVTExecution', socketId, GroupName, TrajectoryFileName, ExecutionNumber);
