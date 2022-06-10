function [errorCode] = XYLineArcExecution(socketId, GroupName, TrajectoryFileName, Velocity, Acceleration, ExecutionNumber)
%XYLineArcExecution :  XY trajectory execution
%
%	[errorCode] = XYLineArcExecution(socketId, GroupName, TrajectoryFileName, Velocity, Acceleration, ExecutionNumber)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		cstring TrajectoryFileName
%		double Velocity
%		double Acceleration
%		int32 ExecutionNumber
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName, TrajectoryFileName] = calllib('XPS_Q8_drivers', 'XYLineArcExecution', socketId, GroupName, TrajectoryFileName, Velocity, Acceleration, ExecutionNumber);
