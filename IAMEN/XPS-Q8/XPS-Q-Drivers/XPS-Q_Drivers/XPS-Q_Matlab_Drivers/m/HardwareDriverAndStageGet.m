function [errorCode, DriverName, StageName] = HardwareDriverAndStageGet(socketId, PlugNumber)
%HardwareDriverAndStageGet :  Smart hardware
%
%	[errorCode, DriverName, StageName] = HardwareDriverAndStageGet(socketId, PlugNumber)
%
%	* Input parameters :
%		int32 socketId
%		int32 PlugNumber
%	* Output parameters :
%		int32 errorCode
%		cstring DriverName
%		cstring StageName


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
DriverName = '';
for i = 1:103
	DriverName = [DriverName '          '];
end
StageName = '';
for i = 1:103
	StageName = [StageName '          '];
end

% lib call
[errorCode, DriverName, StageName] = calllib('XPS_Q8_drivers', 'HardwareDriverAndStageGet', socketId, PlugNumber, DriverName, StageName);
