function [errorCode] = XYZSplineExecution(socketId, GroupName, TrajectoryFileName, Velocity, Acceleration)
%XYZSplineExecution :  XYZ trajectory execution
%
%	[errorCode] = XYZSplineExecution(socketId, GroupName, TrajectoryFileName, Velocity, Acceleration)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		cstring TrajectoryFileName
%		double Velocity
%		double Acceleration
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GroupName, TrajectoryFileName] = calllib('XPS_Q8_drivers', 'XYZSplineExecution', socketId, GroupName, TrajectoryFileName, Velocity, Acceleration);
