function [errorCode] = MultipleAxesPVTExecution(socketId, GroupName, TrajectoryFileName, ExecutionNumber)
%MultipleAxesPVTExecution :  Multiple axes PVT trajectory execution
%
%	[errorCode] = MultipleAxesPVTExecution(socketId, GroupName, TrajectoryFileName, ExecutionNumber)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		cstring TrajectoryFileName
%		int32 ExecutionNumber
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName, TrajectoryFileName] = calllib('XPS_Q8_drivers', 'MultipleAxesPVTExecution', socketId, GroupName, TrajectoryFileName, ExecutionNumber);
