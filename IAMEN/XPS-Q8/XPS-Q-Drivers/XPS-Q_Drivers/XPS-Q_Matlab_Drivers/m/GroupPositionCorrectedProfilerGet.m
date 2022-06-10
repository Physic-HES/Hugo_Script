function [errorCode, CorrectedProfilerPositionX, CorrectedProfilerPositionY] = GroupPositionCorrectedProfilerGet(socketId, GroupName, PositionX, PositionY)
%GroupPositionCorrectedProfilerGet :  Return corrected profiler positions
%
%	[errorCode, CorrectedProfilerPositionX, CorrectedProfilerPositionY] = GroupPositionCorrectedProfilerGet(socketId, GroupName, PositionX, PositionY)
%
%	* Input parameters :
%		int32 socketId
%		cstring GroupName
%		double PositionX
%		double PositionY
%	* Output parameters :
%		int32 errorCode
%		doublePtr CorrectedProfilerPositionX
%		doublePtr CorrectedProfilerPositionY


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
CorrectedProfilerPositionX = 0;
CorrectedProfilerPositionY = 0;

% lib call
[errorCode, GroupName, CorrectedProfilerPositionX, CorrectedProfilerPositionY] = calllib('XPS_Q8_drivers', 'GroupPositionCorrectedProfilerGet', socketId, GroupName, PositionX, PositionY, CorrectedProfilerPositionX, CorrectedProfilerPositionY);
