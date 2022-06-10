function [errorCode, FileName, Velocity, Acceleration, CurrentElementNumber] = XYZSplineParametersGet(socketId, GroupName)
%XYZSplineParametersGet :  XYZ trajectory get parameters
%
%	[errorCode, FileName, Velocity, Acceleration, CurrentElementNumber] = XYZSplineParametersGet(socketId, GroupName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%	* Output parameters :
%		int32 errorCode
%		cstring FileName
%		doublePtr Velocity
%		doublePtr Acceleration
%		int32Ptr CurrentElementNumber


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
FileName = '';
for i = 1:103
	FileName = [FileName '          '];
end
Velocity = 0;
Acceleration = 0;
CurrentElementNumber = 0;

% lib call
[errorCode, GroupName, FileName, Velocity, Acceleration, CurrentElementNumber] = calllib('XPS_Q8_drivers', 'XYZSplineParametersGet', socketId, GroupName, FileName, Velocity, Acceleration, CurrentElementNumber);
