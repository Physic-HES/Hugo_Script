function [errorCode, CorrectedProfilerPositionX, CorrectedProfilerPositionY, CorrectedProfilerPositionZ] = XYZGroupPositionCorrectedProfilerGet(socketId, GroupName, PositionX, PositionY, PositionZ)
%XYZGroupPositionCorrectedProfilerGet :  Return corrected profiler positions
%
%	[errorCode, CorrectedProfilerPositionX, CorrectedProfilerPositionY, CorrectedProfilerPositionZ] = XYZGroupPositionCorrectedProfilerGet(socketId, GroupName, PositionX, PositionY, PositionZ)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		double PositionX
%		double PositionY
%		double PositionZ
%	* Output parameters :
%		int32 errorCode
%		doublePtr CorrectedProfilerPositionX
%		doublePtr CorrectedProfilerPositionY
%		doublePtr CorrectedProfilerPositionZ


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
CorrectedProfilerPositionX = 0;
CorrectedProfilerPositionY = 0;
CorrectedProfilerPositionZ = 0;

% lib call
[errorCode, GroupName, CorrectedProfilerPositionX, CorrectedProfilerPositionY, CorrectedProfilerPositionZ] = calllib('XPS_Q8_drivers', 'XYZGroupPositionCorrectedProfilerGet', socketId, GroupName, PositionX, PositionY, PositionZ, CorrectedProfilerPositionX, CorrectedProfilerPositionY, CorrectedProfilerPositionZ);
